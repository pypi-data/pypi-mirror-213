import os
from importlib.metadata import version

import click
from bpkio_api import BroadpeakIoApi
from bpkio_api.credential_provider import TenantProfileProvider
from bpkio_api.models import BaseResource

from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.logger import get_child_logger

logger = get_child_logger("init")

user_agent = f"bpkio-cli/{version('bpkio-cli')}"


def initialize(
    requires_api: bool,
    tenant: str | int | None = None,
    use_cache: bool = True,
    use_prompts: bool = True,
) -> AppContext:
    """Function that initialises the CLI

    If a tenant label or ID is provided, the CLI will be initialised for that tenant.
    Otherwise, the CLI will be initialised with the last tenant used (and stored in
    a `.tenant` file).

    Successful initialisation requires that there is a profile in ~/.bpkio/tenants
    for that tenant.

    Args:
        tenant (str | int): Name of the CLI profile or ID of the tenant

    Raises:
        click.Abort: if no tenant profile could be found in the ~/.bpkio/tenants file

    Returns:
        AppContext: The config for the app
    """
    if not tenant:
        try:
            with open(".tenant") as f:
                tenant = f.read().strip()
                logger.debug(f"File '.tenant' contains label '{tenant}'")
        except Exception:
            tenant = None
    else:
        tenant = str(tenant)

    # Define a file to store a recording of actions
    session_file = None
    session_sentinel = os.path.expanduser("~/.bpkio/cli_session")
    if os.path.exists(session_sentinel):
        # open it and extract the path to the session file.
        with open(session_sentinel, "r") as f:
            session_file = f.read()

    if requires_api:
        api = BroadpeakIoApi(
            tenant=tenant,
            use_cache=use_cache,
            session_file=session_file,
            user_agent=user_agent,
        )
        app_context = AppContext(api=api, tenant_provider=TenantProfileProvider())
        app_context.config.set_temporary("use_prompts", use_prompts)

        if app_context.config.get("verbose", int) > 0:
            full_tenant = api.get_self_tenant()
            app_context.tenant = full_tenant
        else:
            app_context.tenant = BaseResource(id=api.get_tenant_id())

        # Check size of the session recorder, in case it was left on
        # from a previous run.
        if api.session_recorder.is_active():
            click.secho(
                "⚠️  WARNING: Active recording session (with %s records)"
                % api.session_recorder.size(),
                fg="magenta",
                err=True,
            )

        return app_context
