import os

import click
import cloup

from bpkio_cli.writers.breadcrumbs import display_context


class DefaultLastCommandGroup(cloup.Group):
    """allow a default command for a group"""

    def resolve_command(self, ctx, args):
        if args[0] not in self.list_commands(ctx) and args[0] not in self.alias2name:
            last_command = self._get_last_command()
            if last_command:
                display_context(f"Using last command: '{last_command}'")
                args.insert(0, last_command)

        return super(DefaultLastCommandGroup, self).resolve_command(ctx, args)

    def _get_last_command(self):
        if os.path.exists(".last_command"):
            with open(".last_command") as f:
                return f.read()
        return None
