from typing import Optional


def select_markers(level: Optional[int] = None):
    standard_markers = markers(level)
    standard_markers["pointer"] = _indent(">", level + 1 if level else 1)

    return standard_markers


def markers(level: Optional[int] = None):
    return {
        "qmark": _indent("?", level),
        "amark": _indent("*", level),
    }


def _indent(s: str, level: Optional[int] = None):
    if not level:
        level = 0

    return "  " * level + s


# Keybindings


