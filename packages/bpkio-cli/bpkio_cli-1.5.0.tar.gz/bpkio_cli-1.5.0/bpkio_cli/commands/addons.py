import os

import click
import cloup

plugin_folder = os.path.join(os.path.dirname(__file__), "../../plugins")


class AddonGroup(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns[name]


@cloup.command(cls=AddonGroup, help="Other functionality provided through plugins")
def addons():
    pass
