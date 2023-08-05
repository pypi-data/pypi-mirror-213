from typing import Optional

import click


class Colorizer:
    @staticmethod
    def node(text):
        return click.style(text, fg="white", bold=True)

    @staticmethod
    def attr(text):
        return click.style(text, fg="bright_blue")

    @staticmethod
    def value(text):
        return click.style(text, fg="cyan")

    @staticmethod
    def markup(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def past(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def future(text):
        return click.style(text, fg="green", dim=False)

    @staticmethod
    def high1(text):
        return click.style(text, fg="yellow")

    @staticmethod
    def high2(text):
        return click.style(text, fg="yellow", bold=True)

    @staticmethod
    def high3(text):
        return click.style(text, fg="magenta", bold=True)

    @staticmethod
    def url(text):
        return click.style(text, fg="yellow", italic=True)

    @staticmethod
    def url2(text):
        return click.style(text, fg="green", italic=True, underline=True)

    @staticmethod
    def expand(text):
        return click.style(text, fg="bright_black", italic=True)

    @staticmethod
    def make_separator(
        text: Optional[str] = None, length: Optional[int] = None, mode=None
    ):
        if text:
            dashes = "-" * len(text)
        else:
            if not length:
                length = 30
            dashes = "-" * length

        if mode == "xml":
            dashes = f"<!-- {dashes} -->"
        if mode == "hls":
            dashes = f"## {dashes}"

        return Colorizer.high3(dashes)
