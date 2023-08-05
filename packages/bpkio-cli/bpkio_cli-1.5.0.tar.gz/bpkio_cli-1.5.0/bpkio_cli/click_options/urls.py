import functools

import click

from bpkio_cli.utils.urls import validate_ipv4_or_domain


# Common parameters for READ and POLL
def url_options(fn):
    @click.option(
        "-s",
        "--sub",
        type=int,
        default=None,
        help="For HLS, read a sub-playlist (by index - as given by the `read ID --table` option with the main playlist)",
    )
    @click.option(
        "-u",
        "--url",
        type=str,
        default=None,
        help="Full URL of URL sub-path (for asset catalogs) to fetch",
    )
    @click.option(
        "-f",
        "--fqdn",
        type=str,
        default=None,
        is_flag=False,
        flag_value="SELECT",
        help="FQDN to use instead of the resource's own. "
        + "This option only applies to Services, and is typically "
        + "used to redirect the call through a CDN",
        callback=validate_fqdn,
    )
    @click.option(
        "-ua",
        "--user-agent",
        type=str,
        default=None,
        is_flag=False,
        flag_value="SELECT",
        help="Choose a different user agent to use when requesting the content. "
        + "Defaults to a standard Mozilla user agent if not set. "
        + "The value for the option is the label of a user-agent in the cli.cfg file, "
        + "the user-agent string itself, or leave empty to be presented with a choice.",
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def validate_fqdn(ctx, param, value):
    if value and value != "SELECT":
        valid = validate_ipv4_or_domain(value)
        if not valid:
            raise click.BadParameter("FQDN must be a valid IPv4 or domain name")
    return value
