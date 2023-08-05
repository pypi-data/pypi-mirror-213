# from __future__ import absolute_import

import logging

import click
import cloup

import bpkio_cli.commands as commands
from bpkio_cli.click_mods.default_last_command import DefaultLastCommandGroup
from bpkio_cli.commands.configure import init
from bpkio_cli.core.config_provider import ConfigProvider
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.logger import (
    get_child_logger,
    get_level_names,
    set_console_logging_level,
)
from bpkio_cli.writers.breadcrumbs import display_tenant_info

logger = get_child_logger("cli")

LOG_LEVEL = None
LOG_SDK = False


SETTINGS = cloup.Context.settings(
    formatter_settings=cloup.HelpFormatter.settings(theme=cloup.HelpTheme.dark())
)


@cloup.group(
    show_subcommand_aliases=True, context_settings=SETTINGS, cls=DefaultLastCommandGroup
)
@click.version_option(
    package_name="bpkio_cli", prog_name="Command Line helpers for broadpeak.io"
)
@click.option("-t", "--tenant", help="Identifier of the tenant profile to impersonate")
@click.option(
    "--log-level",
    type=click.Choice(get_level_names()),
    required=False,
    show_default=True,
    help="Set the log level",
)
@click.option(
    "--log-sdk",
    type=bool,
    is_flag=True,
    required=False,
    default=False,
    show_default=True,
    help="Log messages from the underlying API client",
)
@click.option(
    "-cc / -nc",
    "--cache / --no-cache",
    "use_cache",
    is_flag=True,
    default=True,
    show_default=True,
    help="Enable or disable resource caches",
)
@click.option(
    "-pp / -np",
    "--prompts / --no-prompts",
    "use_prompts",
    is_flag=True,
    default=True,
    show_default=True,
    help="Enable or disable the use of prompts to ask for some information (where supported)",
)
@click.pass_context
def bic(ctx, tenant, log_level, log_sdk, use_cache, use_prompts):
    if log_level or LOG_LEVEL:
        set_console_logging_level(
            log_level or LOG_LEVEL, include_sdk=log_sdk or LOG_SDK
        )

    requires_api = True
    if ctx.invoked_subcommand in ["init", "configure", "record"]:
        requires_api = False

    app_context = initialize(
        tenant=tenant,
        use_cache=use_cache,
        use_prompts=use_prompts,
        requires_api=requires_api,
    )

    if app_context and ctx.invoked_subcommand not in ["init", "configure"]:
        display_tenant_info(app_context.tenant)

    # TODO - validate the token in the initialisation of BroadpeakApi
    ctx.obj = app_context

    @ctx.call_on_close
    def close_cleanly():
        try:
            # Save the cache to disk
            app_context.cache.save()

            # Save the current command
            with open(".last_command", "w") as f:
                f.write(ctx.invoked_subcommand)

        except Exception as e:
            pass


bic.section("Configuration", commands.hello, init, commands.configure)

commands.add_sources_section(bic)
commands.add_services_section(bic)

bic.section(
    "Other resources",
    commands.profile,
    commands.url,
)

bic.section(
    "Account resources",
    commands.add_tenants_commands(),
    commands.add_users_commands(),
    commands.consumption,
)

bic.section(
    "Advanced", commands.package, commands.record, commands.memory, commands.addons
)


def debug_entry_point():
    global LOG_LEVEL
    LOG_LEVEL = logging.DEBUG
    global LOG_SDK
    LOG_SDK = True
    bic(obj={})


def safe_entry_point():
    try:
        bic()
    except Exception as e:
        if hasattr(e, "status_code"):
            st = " [{}] ".format(e.status_code)
        else:
            st = ""
        msg = "{}: {}{}".format(e.__class__.__name__, st, e)
        click.secho(msg, fg="red")

        if hasattr(e, "original_message"):
            click.secho("  > {}".format(e.original_message), fg="red")


if __name__ == "__main__":
    debug_entry_point()
