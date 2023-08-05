from typing import List, Optional
from urllib.parse import urljoin, urlparse, urlunparse

import click
import InquirerPy.inquirer as inquirer
from bpkio_api.helpers.handlers import ContentHandler, factory
from bpkio_api.models import (
    AdInsertionService,
    AdServerSourceIn,
    AssetCatalogSourceIn,
    BaseResource,
    SourceIn,
    SourceType,
    VirtualChannelService,
)

import bpkio_cli.utils.inquirer as inqdef
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import ConfigProvider
from bpkio_cli.utils.urls import add_query_parameters, validate_ipv4_or_domain

NEW = "-- add new --"
DELETED = "__DELETED__"
UNSET = "__UNSET__"


def get_source_handler(
    source: SourceIn,
    extra_url: Optional[str],
    subplaylist_index: Optional[int],
    user_agent: Optional[str],
) -> ContentHandler:
    if isinstance(source, AssetCatalogSourceIn):
        # Ask for extra portion of URL if it wasn't supplied
        if not extra_url:
            extra_url = ask_for_asset_catalog_sub_path(source)

    url_to_read = source.make_full_url(extra_url)

    if isinstance(source, AdServerSourceIn):
        # Fill query parameters
        if not extra_url or "?" not in url_to_read:
            filled_params = ask_for_adserver_query_params(source)
            url_to_read = add_query_parameters(url_to_read, filled_params)

    if user_agent == "SELECT":
        user_agent = ask_for_user_agent(source)

    handler: ContentHandler = factory.create_handler(
        url_to_read, user_agent=ConfigProvider().get_user_agent(user_agent)
    )
    if subplaylist_index:
        if not handler.has_children():
            raise click.UsageError(
                "`--sub` cannot be used with this source, as it has no children URLs"
            )
        handler = handler.get_child(subplaylist_index)

    return handler


def get_service_handler(
    service,
    api,
    replacement_fqdn: Optional[str],
    extra_url: Optional[str],
    subplaylist_index: Optional[int],
    user_agent: Optional[str],
) -> ContentHandler:
    """Calculates the URL to call for a Service, based on its type and Source"""
    url_to_read = service.make_full_url()

    if isinstance(service, AdInsertionService):
        source_type = service.source.type
        source_id = service.source.id

        if source_type == SourceType.ASSET_CATALOG:
            # Ask for extra portion of URL if it wasn't supplied
            if not extra_url:
                source = api.sources.asset_catalog.retrieve(source_id)
                extra_url = ask_for_asset_catalog_sub_path(source)

            url_to_read = urljoin(service.url, extra_url)

    # replace the fqdn if necessary
    if replacement_fqdn:
        if replacement_fqdn == "SELECT":
            replacement_fqdn = ask_for_fqdn(service)

        parsed_url = urlparse(url_to_read)
        url_to_read = urlunparse(parsed_url._replace(netloc=replacement_fqdn))

    # In case it's a service with ad insertion, and the ad server has query params,
    # prompt for values for the ones expected to be passed through
    ad_config = None
    if isinstance(service, AdInsertionService):
        ad_config = get_first_matching_key_value(
            service, ["vodAdInsertion", "liveAdPreRoll", "liveAdReplacement"]
        )
    if isinstance(service, VirtualChannelService):
        if service.adBreakInsertion:
            ad_config = service.adBreakInsertion

    if ad_config and ad_config.adServer:
        queries = {}
        if extra_url and "?" in extra_url:
            query_string = extra_url.split("?")[1]
            queries = {k: v for k, v in (x.split("=") for x in query_string.split("&"))}

        filled_params = ask_for_adserver_query_params(
            ad_config.adServer, existing_params=queries, for_service=True
        )
        url_to_read = add_query_parameters(url_to_read, filled_params)

    if user_agent == "SELECT":
        user_agent = ask_for_user_agent(service)

    handler: ContentHandler = factory.create_handler(
        url_to_read,
        from_url_only=True,
        user_agent=ConfigProvider().get_user_agent(user_agent),
    )
    if subplaylist_index:
        if not handler.has_children():
            raise click.UsageError(
                "`--sub` cannot be used with this source, as it has no children URLs"
            )
        handler = handler.get_child(subplaylist_index)

    return handler


def get_first_matching_key_value(resource: BaseResource, possible_keys: List[str]):
    for key in possible_keys:
        if getattr(resource, key):
            return getattr(resource, key)
    return None


def ask_for_adserver_query_params(
    adserver: AdServerSourceIn, existing_params={}, for_service=False
):
    obj: AppContext = click.get_current_context().obj

    section_title_shown = False

    metadata_cache = obj.cache
    filled_params = dict()
    params = adserver.queries

    if params:
        params = params.split("&")
        for p in params:
            parts = p.split("=")
            if len(parts) == 2:
                (k, val) = parts
            else:
                k = (parts[0],)
                val = "=".join(parts[1:])

            if val.startswith("$arg_"):
                input_param = val.replace("$arg_", "")
                # determine output param name
                if for_service:
                    param_to_fill = input_param
                else:
                    param_to_fill = k

                cached_values = metadata_cache.get_metadata(adserver, input_param)

                if k in existing_params:
                    cached_values.insert(0, existing_params[k])

                input_val = UNSET

                if obj.config.get("use_prompts"):
                    if not section_title_shown:
                        click.secho(
                            "\nQuery params to pass to the ad server", fg="white"
                        )
                        section_title_shown = True

                    while input_val in [DELETED, UNSET]:
                        if cached_values:
                            input_val_prompt = inquirer.select(
                                message=f"Parameter '{input_param}': ",
                                choices=cached_values + [NEW],
                                multiselect=False,
                                default=cached_values[0],
                                long_instruction="Key bindings: 'd' = delete the selected value | "
                                "'ctrl-s' = skip all prompts, using last or default value",
                                **inqdef.select_markers(),
                            )

                            @input_val_prompt.register_kb("d")
                            def _handle_delete(event):
                                choice_value = input_val_prompt.result_value

                                metadata_cache.remove_metadata(
                                    adserver, input_param, choice_value
                                )
                                event.app.exit(result=DELETED)

                            @input_val_prompt.register_kb("c-s")
                            def _handle_skip_all(event):
                                choice_value = input_val_prompt.result_value

                                obj.config.set_temporary("use_prompts", False)
                                click.secho(choice_value, fg="bright_blue")
                                event.app.exit(result=choice_value)

                            input_val = input_val_prompt.execute()

                        if not cached_values:
                            input_val_prompt = inquirer.text(
                                message=f"Parameter '{input_param}'",
                                **inqdef.markers(0),
                                long_instruction="Key bindings: 'ctrl-s' = skip all prompts, using last or default value",
                            )

                            @input_val_prompt.register_kb("c-s")
                            def _handle_skip_all(event):
                                obj.config.set_temporary("use_prompts", False)
                                event.app.exit(result="")

                            input_val = input_val_prompt.execute()

                        if input_val == NEW:
                            input_val = inquirer.text(
                                message="New value: ", **inqdef.markers(1)
                            ).execute()

                else:
                    if cached_values:
                        input_val = cached_values[0]
                    else:
                        input_val = ""

                    click.secho(f"> Parameter '{input_param}': ", fg="white", nl=False)
                    click.secho(input_val, fg="blue", bold=True)

                filled_params[param_to_fill] = input_val

                if input_val is not None and input_val != "":
                    metadata_cache.record_metadata(adserver, input_param, input_val)
    return filled_params


def ask_for_asset_catalog_sub_path(source: AssetCatalogSourceIn):
    extra_url = source.assetSample

    obj = click.get_current_context().obj

    metadata_cache = obj.cache
    cached_values = metadata_cache.get_metadata(source, "subPath")

    extra_url = UNSET

    if obj.config.get("use_prompts"):
        while extra_url in [UNSET, DELETED]:
            if cached_values:
                extra_url_prompt = inquirer.select(
                    message="Sub-path",
                    choices=cached_values + [NEW],
                    multiselect=False,
                    default=cached_values[0],
                    long_instruction="Keyboard: 'd' = delete the selected value | "
                    "'ctrl-s' = skip all prompts, using last or default value",
                    **inqdef.select_markers(),
                )

                @extra_url_prompt.register_kb("d")
                def _handle_delete(event):
                    choice_value = extra_url_prompt.result_value

                    metadata_cache.remove_metadata(source, "subPath", choice_value)
                    event.app.exit(result=DELETED)

                @extra_url_prompt.register_kb("c-s")
                def _handle_skip_all(event):
                    choice_value = extra_url_prompt.result_value
                    obj.config.set_temporary("use_prompts", False)
                    click.secho(choice_value, fg="bright_blue")

                    event.app.exit(result=choice_value)

                extra_url = extra_url_prompt.execute()

            if not cached_values or extra_url == NEW:
                extra_url = inquirer.text(
                    message="Sub-path (defaulting to the asset sample, if empty)",
                    default=source.assetSample,
                    **inqdef.markers(),
                ).execute()

    else:
        if cached_values:
            extra_url = cached_values[0]
        else:
            extra_url = source.assetSample

        click.secho("> Sub-path: ", fg="white", nl=False)
        click.secho(extra_url, fg="blue", bold=True)

    metadata_cache.record_metadata(source, "subPath", extra_url)

    return extra_url


def ask_for_fqdn(service):
    fqdn = None
    obj: AppContext = click.get_current_context().obj
    metadata_cache = obj.cache
    cached_fqdns = metadata_cache.get_metadata(service, "fqdn")

    if obj.config.get("use_prompts"):
        if cached_fqdns:
            fqdn = inquirer.select(
                message="Domain name (for CDN)",
                choices=cached_fqdns + [NEW],
                multiselect=False,
                default=cached_fqdns[0],
                **inqdef.select_markers(),
            ).execute()

        if not cached_fqdns or fqdn == NEW:
            fqdn = inquirer.text(
                message="Domain name (for CDN)",
                default="",
                validate=lambda x: validate_ipv4_or_domain(x),
                invalid_message="Must be a well-formed domain name or IP address",
                **inqdef.markers(0),
            ).execute()

    else:
        if cached_fqdns:
            fqdn = cached_fqdns[0]
        else:
            fqdn = "CUSTOM_FQDN"

        click.secho("> FQDN: ", fg="white", nl=False)
        click.secho(fqdn, fg="blue", bold=True)

    metadata_cache.record_metadata(service, "fqdn", fqdn)

    return fqdn


def ask_for_user_agent(resource):
    ua = UNSET
    obj: AppContext = click.get_current_context().obj
    metadata_cache = obj.cache
    cached_useragents = metadata_cache.get_metadata(resource, "user_agent")

    if obj.config.get("use_prompts"):
        click.echo()
        while ua in [UNSET, DELETED]:
            if cached_useragents:
                ua_prompt = inquirer.select(
                    message="User agent to use: ",
                    choices=cached_useragents + [NEW],
                    multiselect=False,
                    default=cached_useragents[0],
                    long_instruction="Keyboard: 'd' = delete the selected value | "
                    "'ctrl-s' = skip all prompts, using last or default value",
                    **inqdef.select_markers(),
                )

                @ua_prompt.register_kb("d")
                def _handle_delete(event):
                    choice_value = ua_prompt.result_value

                    metadata_cache.remove_metadata(resource, "user_agent", choice_value)
                    event.app.exit(result=DELETED)

                @ua_prompt.register_kb("c-s")
                def _handle_skip_all(event):
                    choice_value = ua_prompt.result_value
                    obj.config.set_temporary("use_prompts", False)
                    click.secho(choice_value, fg="bright_blue")

                    event.app.exit(result=choice_value)

                ua = ua_prompt.execute()

            if not cached_useragents or ua == NEW:
                ua = inquirer.text(
                    message="User agent (label or full string)",
                    default="",
                    **inqdef.markers(0),
                ).execute()

    else:
        if cached_useragents:
            ua = cached_useragents[0]
        else:
            ua = None

        click.secho("> User-Agent: ", fg="white", nl=False)
        click.secho(ua, fg="blue", bold=True)

    metadata_cache.record_metadata(resource, "user_agent", ua)

    return ua
