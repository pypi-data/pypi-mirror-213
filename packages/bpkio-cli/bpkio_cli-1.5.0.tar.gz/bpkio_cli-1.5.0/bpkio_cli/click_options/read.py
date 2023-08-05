import functools

import click


# Common parameters for READ and POLL
def read_options(fn):
    @click.option(
        "--raw",
        is_flag=True,
        type=bool,
        default=False,
        help="Get the raw content, unchanged",
    )
    @click.option(
        "--top", type=int, default=0, help="Only display the first N lines"
    )
    @click.option(
        "--tail", type=int, default=0, help="Only display the last N lines"
    )
    @click.option(
        "--pager/--no-pager",
        type=bool,
        is_flag=True,
        default=None,
        help="Display through a pager (to allow scrolling). If the flag is not set, a pager will automatically be used if the content is too long to fit on screen",
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
