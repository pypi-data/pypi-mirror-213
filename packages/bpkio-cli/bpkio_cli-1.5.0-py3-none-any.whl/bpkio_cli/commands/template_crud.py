import json as j
import re
from typing import List
from urllib.parse import quote_plus

import bpkio_api.mappings as mappings
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder
from bpkio_api.models import ServiceIn, SourceIn

import bpkio_cli.click_options as bic_options
from bpkio_cli.click_mods.group_rest_resource import ApiResourceGroup
from bpkio_cli.commands.package import package_resources
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.resource_trail import ResourceTrail, UnknownResourceError
from bpkio_cli.utils.editor import edit_payload
from bpkio_cli.utils.profile_maker import make_transcoding_profile
from bpkio_cli.utils.url_builders import get_service_handler, get_source_handler
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.content_display import display_content
from bpkio_cli.writers.players import StreamPlayer
from bpkio_cli.writers.tables import display_table


def create_resource_group(
    name: str,
    resource_class: type,
    endpoint_path: List[str],
    title: str | None = None,
    aliases: List[str] = [],
    default_fields=["id", "name", "type"],
    with_content_commands: List[str] = [],
    extra_commands: List[cloup.Command] = [],
):
    """Generates a group of CLI commands for CRUD-based resources

    Args:
        name (str): The name of the command group
        aliases (List[str], optional): Aliases for the command name. Defaults to none.
        default_fields (list, optional): Base resource fields used for table displays.
            Defaults to ["id", "name", "type"].
        endpoint_path (List[str]): List of the endpoint names that make the path of the
            corresponding api class (eg. ["sources", "virtual-channel"])
        with_content_commands (bool | List[str]): Defines whether the group contains
            commands for handling resource content (for sources and services)
        extra_commands (list): List of additional commands to add

    Returns:
        cloup.Group: The MultiCommand group with all its nested commands
    """
    resource_title = title if title else str.title(name.replace("-", " "))
    if len(endpoint_path) > 1:
        parent_resource_title = re.sub("s$", "", endpoint_path[0])
        resource_title = f"{resource_title} {parent_resource_title}"

    sections = []

    # === HELPER functions ===

    def get_api_endpoint(path=endpoint_path):
        api = click.get_current_context().obj.api
        endpoint = api
        for p in path:
            endpoint = getattr(endpoint, p)
        return endpoint

    def retrieve_resource(id: int | str | None = None):
        ctx = click.get_current_context()
        resource_context: ResourceTrail = ctx.obj.resources
        if not id:
            id = resource_context.last()
        endpoint = get_api_endpoint()
        resource = endpoint.retrieve(id)

        # Record the resource
        if ctx.obj.cache and hasattr(resource, "id"):
            ctx.obj.cache.record(resource)

        return resource

    def get_content_handler(
        resource,
        replacement_fqdn=None,
        extra_url=None,
        subplaylist_index=None,
        user_agent=None,
    ):
        api = click.get_current_context().obj.api

        if isinstance(resource, SourceIn):
            return get_source_handler(
                resource,
                extra_url=extra_url,
                subplaylist_index=subplaylist_index,
                user_agent=user_agent,
            )

        if isinstance(resource, ServiceIn):
            return get_service_handler(
                resource,
                replacement_fqdn=replacement_fqdn,
                extra_url=extra_url,
                subplaylist_index=subplaylist_index,
                api=api,
                user_agent=user_agent,
            )

    # === GROUP ===

    @cloup.group(
        name=name,
        help=f"Manage {resource_title}s",
        aliases=aliases,
        cls=ApiResourceGroup,
        show_subcommand_aliases=True,
        resource_class=resource_class,
    )
    @cloup.argument(
        "id",
        metavar=f"<{name.replace('-', '_')}_id>",
        help=(
            f"The identifier of the {resource_title} to work with. "
            f"Leave empty for commands operating on a list of {resource_title}s."
            "You can use $ and @ notation to refer to previously selected resources"
        ),
    )
    @click.pass_context
    @SessionRecorder.do_not_record
    def resource_group(ctx, id):
        if id:
            resource = retrieve_resource(id)
            if ctx.invoked_subcommand != "get":
                display_resource_info(resource)

    # === CRUD Commands ===

    # --- LIST Command
    @cloup.command(help=f"List all {resource_title}s", aliases=["ls"])
    @bic_options.json
    @bic_options.list(default_fields=default_fields)
    @click.pass_obj
    def list(obj: AppContext, json, select_fields, sort_fields, **kwargs):
        endpoint = get_api_endpoint()
        resources = endpoint.list()

        obj.response_handler.treat_list_resources(
            resources, select_fields=select_fields, sort_fields=sort_fields, json=json
        )

    # --- GET Commmand
    @cloup.command(aliases=["retrieve"], help=f"Get a specific {resource_title} by ID")
    @bic_options.json
    @click.option(
        "--table/--no-table",
        "with_table",
        is_flag=True,
        default=True,
        help="Add or hide summary information about the content of the resource",
    )
    @click.pass_context
    def get(ctx, json: bool, with_table: bool):
        resource = retrieve_resource()

        ctx.obj.response_handler.treat_single_resource(resource, json=json)

        # then show the summary table (if there is one)
        if with_table and not json:
            try:
                ctx.invoke(table, header=False)
            except NameError:
                pass

    # --- JSON Commmand
    @cloup.command(
        help=f"Get the JSON representation of a single {resource_title}",
    )
    @click.pass_obj
    def json(obj: AppContext):
        resource = retrieve_resource()
        obj.response_handler.treat_single_resource(resource, json=True)

    # --- SEARCH Command
    @cloup.command(
        help=f"Retrieve a list of all {resource_title}s "
        "that match given terms in all or selected fields"
    )
    @bic_options.search
    @bic_options.json
    @bic_options.list(default_fields=default_fields)
    @click.pass_obj
    def search(
        obj: AppContext,
        single_term,
        search_terms,
        search_fields,
        sort_fields,
        json,
        select_fields,
    ):
        search_def = bic_options.validate_search(
            single_term, search_terms, search_fields
        )

        endpoint = get_api_endpoint()
        resources = endpoint.search(filters=search_def)

        obj.response_handler.treat_list_resources(
            resources, select_fields=select_fields, sort_fields=sort_fields, json=json
        )

    # --- DELETE Commmand
    @cloup.command(aliases=["del"], help=f"Delete a specific {resource_title} by ID")
    @click.confirmation_option(prompt="Are you sure you want to delete this resource?")
    @click.pass_context
    def delete(ctx):
        resource = retrieve_resource()

        endpoint = get_api_endpoint()
        endpoint.delete(resource.id)

        # remove from cache
        ctx.obj.cache.remove(resource)

        click.secho(f"Resource {resource.id} deleted", fg="green")

    # --- UPDATE Command
    @cloup.command(aliases=["put"], help=f"Update a {resource_title}")
    @click.pass_context
    def update(ctx):
        resource = retrieve_resource()
        resource_id = resource.id

        # remap to an input model
        resource = mappings.to_input_model(resource)

        updated_resource = edit_payload(resource)

        endpoint = get_api_endpoint()
        # TODO - try to parse into the resource class (otherwise can only work with specific resource sub-types)
        endpoint.update(resource_id, updated_resource)

        click.secho(f"Resource {resource_id} updated", fg="green")

    # --- DUPLICATE Command
    @cloup.command(aliases=["copy"], help=f"Duplicate a {resource_title}")
    @click.option(
        "-e",
        "--edit",
        help="Edit the duplicated resource before saving it",
        is_flag=True,
        default=False,
    )
    @click.pass_obj
    def duplicate(obj, edit):
        resource = retrieve_resource()
        endpoint = obj.api.root_endpoint_for_resource(resource)

        resource.name = resource.name + " (copy)"

        # remap to an input model
        resource = mappings.to_input_model(resource)

        if edit:
            resource = edit_payload(resource)

        new_resource = endpoint.create(resource)

        obj.response_handler.treat_single_resource(new_resource, json=True)

    sections.append(
        cloup.Section(
            "CRUD commands", [list, get, json, search, delete, update, duplicate]
        )
    )

    # === CONTENT Commands ===

    content_section = cloup.Section("Content commands", [])

    if any(x in with_content_commands for x in ["all", "url"]):
        # --- URL Command
        @cloup.command(help="Retrieve the full URL of the resource")
        @bic_options.url
        def url(
            sub: int,
            url: str,
            fqdn: str,
            user_agent: str,
            **kwargs,
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            if handler:
                click.secho(handler.url, fg="yellow")

        content_section.add_command(url)

    if any(x in with_content_commands for x in ["all", "check"]):
        # --- CHECK Command
        @cloup.command(help=f"Check the validity of an existing {resource_title}")
        @bic_options.json
        @bic_options.list()
        @click.pass_obj
        def check(obj: AppContext, select_fields, sort_fields, json):
            id = obj.resources.last()
            endpoint = get_api_endpoint(endpoint_path[0:1])
            results = endpoint.check_by_id(id)

            obj.response_handler.treat_list_resources(
                results, json=json, select_fields=select_fields, sort_fields=sort_fields
            )

        content_section.add_command(check)

    if any(x in with_content_commands for x in ["all", "table"]):
        # --- TABLE Command
        @cloup.command(help="Provide summary table(s) of the content of the file")
        @bic_options.url
        @click.pass_obj
        def table(
            obj: AppContext,
            sub: int,
            url: str,
            fqdn: str,
            user_agent: str,
            header: bool = True,
            **kwargs,
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if handler:
                try:
                    display_content(
                        handler=handler,
                        max=1,
                        interval=0,
                        table=True,
                        header=header,
                    )
                except BroadpeakIoCliError as e:
                    pass

        content_section.add_command(table)

    if any(x in with_content_commands for x in ["all", "read"]):
        # --- READ Command
        @cloup.command(
            help=f"Load and display the content of a {resource_title}"
            ", optionally highlighted with relevant information"
        )
        @bic_options.read
        @bic_options.url
        @bic_options.table
        @click.pass_obj
        def read(
            obj: AppContext,
            sub: int,
            url: str,
            fqdn: str,
            user_agent: str,
            table: bool,
            raw: bool,
            top: int = 0,
            tail: int = 0,
            header: bool = True,
            pager: bool = False,
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if handler:
                try:
                    display_content(
                        handler=handler,
                        max=1,
                        interval=0,
                        table=table,
                        raw=raw,
                        top=top,
                        tail=tail,
                        header=header,
                        pager=pager,
                    )
                except BroadpeakIoCliError as e:
                    pass

        content_section.add_command(read)

    if any(x in with_content_commands for x in ["all", "poll"]):
        # --- POLL Command
        @cloup.command(
            help=f"Similar to `read`, but regularly re-load the {resource_title}"
            "source's content"
        )
        @bic_options.read
        @bic_options.url
        @bic_options.table
        @bic_options.poll
        def poll(
            sub: int,
            url: str,
            fqdn: str,
            user_agent: str,
            max: int,
            interval: int,
            raw: bool,
            diff: bool,
            top: bool,
            tail: bool,
            clear: bool,
            table: bool,
            pager: bool,
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            if handler:
                display_content(
                    handler,
                    max=max,
                    interval=interval,
                    table=table,
                    raw=raw,
                    diff=diff,
                    top=top,
                    tail=tail,
                    clear=clear,
                    pager=pager,
                )

        content_section.add_command(poll)

    if any(x in with_content_commands for x in ["all", "play"]):
        # --- PLAY Command
        @cloup.command(
            help=f"Open the URL of the {resource_title} in a web player",
            aliases=["open"],
        )
        @bic_options.url
        @click.option(
            "-p",
            "--player",
            default="CONFIG",
            help="The template for a player URL",
            type=str,
            is_flag=False,
            flag_value="CHOICE",
        )
        @click.pass_obj
        def play(
            obj: AppContext, fqdn: str, url: str, user_agent: str, sub: int, player: str
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if player == "CONFIG":
                player = obj.config.get("player")

            if player == "CHOICE":
                player = StreamPlayer.prompt_player()

            # pass a set of useful parameters for placeholder replacement
            # in the player template

            if hasattr(resource, "get_all_fields_and_properties"):
                params = resource.get_all_fields_and_properties()
            else:
                params = dict(params)

            params.update(url=quote_plus(handler.url))

            StreamPlayer().launch(template=player, **params)

        content_section.add_command(play)

    if any(x in with_content_commands for x in ["all", "profile"]):
        # --- PROFILE Command
        @cloup.command(help=f"Create a profile from the {resource_title}")
        @click.option(
            "--table/--no-table",
            "with_table",
            is_flag=True,
            default=False,
            help="Add or hide summary information about the content of the resource",
        )
        @click.option(
            "--save",
            is_flag=True,
            default=False,
            help="Save the profile to a file",
        )
        @bic_options.url
        @click.pass_obj
        def profile(
            obj: AppContext,
            fqdn: str,
            url: str,
            user_agent: str,
            sub: int,
            with_table: bool,
            save: bool,
        ):
            resource = retrieve_resource()
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            profile = make_transcoding_profile(handler)

            if with_table:
                display_table(profile["transcoding"]["jobs"])
            else:
                obj.response_handler.treat_single_resource(profile, json=True)

            if save:
                filename = f"profile_{resource.id}.json"
                with open(filename, "w") as f:
                    j.dump(profile, f, indent=4)
                click.secho(f"Profile saved to {filename}", fg="green")

        content_section.add_command(profile)

    sections.append(content_section)

    # === PACKAGE Commands

    # COMMAND: PACKAGE
    @cloup.command()
    @cloup.option("-o", "--output", type=click.File("w"), required=False, default=None)
    @click.pass_obj
    def package(obj: AppContext, output):
        """Package a service and all its dependencies into a reusable recipe

        Args:
            output (str): Filename of the JSON file to write the package into
        """
        resource = retrieve_resource()

        package_resources([resource], obj.api, output)

    sections.append(cloup.Section("Other commands", [package]))

    # === EXTRA Commands
    # Go through extra commands and add them where relevant...

    for new_command in extra_commands:
        inserted = False
        for section in sections:
            for k in section.commands.keys():
                if k == new_command.name:
                    # ... override an existing one ...
                    section.commands[k] = new_command
                    inserted = True
        if not inserted:
            # ... or add it to the last section
            if new_command.name in ["create", "update", "delete"]:
                for section in sections:
                    if section.title == "CRUD commands":
                        section.add_command(new_command)
                        break
            else:
                sections[-1].add_command(new_command)

    # === END OF GROUP ===
    for section in sections:
        resource_group.add_section(section)

    return resource_group
