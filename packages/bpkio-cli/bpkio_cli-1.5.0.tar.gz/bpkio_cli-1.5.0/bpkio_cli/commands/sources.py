import bpkio_api.models as models
import click
import cloup

import bpkio_cli.click_options as bic_options
from bpkio_cli.commands.creators.sources import create
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.core.app_context import AppContext


def add_sources_section(cli):
    root_endpoint = "sources"
    root: cloup.Group = create_resource_group(
        "source",
        resource_class=models.SourceIn,
        endpoint_path=[root_endpoint],
        aliases=["src", "sources"],
        with_content_commands=["all"],
        default_fields=["id", "name", "type", "format", "url"],
        extra_commands=[create, usage],
    )

    return cli.section(
        "Sources",
        root,
        create_resource_group(
            "asset",
            resource_class=models.AssetSource,
            endpoint_path=[root_endpoint, "asset"],
            aliases=["assets"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["url", "check", "table", "read", "play", "profile"],
            extra_commands=[usage],
        ),
        create_resource_group(
            "live",
            resource_class=models.LiveSource,
            endpoint_path=[root_endpoint, "live"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["all"],
            extra_commands=[usage],
        ),
        create_resource_group(
            "asset-catalog",
            resource_class=models.AssetCatalogSource,
            endpoint_path=[root_endpoint, "asset_catalog"],
            aliases=["catalog", "catalogs"],
            default_fields=["id", "name", "url"],
            with_content_commands=["url", "check", "table", "read", "play", "profile"],
            extra_commands=[usage],
        ),
        create_resource_group(
            "ad-server",
            resource_class=models.AdServerSource,
            endpoint_path=[root_endpoint, "ad_server"],
            aliases=["ads"],
            with_content_commands=["url", "check", "table", "read"],
            default_fields=["id", "name", "url"],
            extra_commands=[usage],
        ),
        create_resource_group(
            "slate",
            resource_class=models.SlateSource,
            endpoint_path=[root_endpoint, "slate"],
            aliases=["slates"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["url", "check", "play"],
            extra_commands=[usage],
        ),
    )


# COMMAND: USAGE
@cloup.command(help="Find all Services that use the source")
@bic_options.json
@bic_options.list(default_fields=["id", "name", "type"])
@click.pass_obj
def usage(obj: AppContext, json, select_fields, sort_fields, **kwargs):
    select_fields = list(select_fields)
    id = obj.resources.last()
    source = obj.api.sources.retrieve(id)

    services = obj.api.services.list()

    selected_services = []
    for service in services:
        svc = obj.api.services.retrieve(service.id)

        if hasattr(svc, "source") and getattr(svc.source, "id") == id:
            selected_services.append(svc)
            select_fields.append("source")

        if hasattr(svc, "replacement") and getattr(svc.replacement, "id") == id:
            selected_services.append(svc)
            select_fields.append("replacement")

        if isinstance(source, models.LiveSource):
            if isinstance(svc, models.VirtualChannelService):
                if svc.baseLive.id == id:
                    selected_services.append(svc)
                    select_fields.append("baseLive")

        if isinstance(source, models.AdServerSource):
            if isinstance(svc, models.AdInsertionService):
                if svc.vodAdInsertion and svc.vodAdInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("vodAdInsertion.adServer.id")
                if svc.liveAdPreRoll and svc.liveAdPreRoll.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdPreRoll.adServer.id")
                if svc.liveAdReplacement and svc.liveAdReplacement.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.adServer.id")

            if isinstance(svc, models.VirtualChannelService):
                if svc.adBreakInsertion and svc.adBreakInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.adServer.id")

        if isinstance(source, models.SlateSource):
            if isinstance(svc, models.AdInsertionService):
                if (
                    svc.liveAdReplacement
                    and svc.liveAdReplacement.gapFiller
                    and svc.liveAdReplacement.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.gapFiller.id")

            if isinstance(svc, models.VirtualChannelService):
                if (
                    svc.adBreakInsertion
                    and svc.adBreakInsertion.gapFiller
                    and svc.adBreakInsertion.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.gapFiller.id")

    if len(selected_services):
        obj.response_handler.treat_list_resources(
            selected_services,
            select_fields=select_fields,
            sort_fields=sort_fields,
            json=json,
        )
    else:
        click.secho("No services found that use this source")
