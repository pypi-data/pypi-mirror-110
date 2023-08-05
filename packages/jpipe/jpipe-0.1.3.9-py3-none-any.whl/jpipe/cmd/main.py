import argparse
import functools
import os
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata


def load_entrypoint(entry_point):
    name = entry_point.value.replace(":", ".")
    modname = ".".join(name.split(".")[:-1])
    mod = __import__(modname)
    components = name.split(".")
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def jpipe_subcommand_callback(
    subcommand, entry_point_func, root_parser, args, remaining_args
):
    argv = [subcommand] + remaining_args
    entry_point_func(argv)


def jpipe_command_callback(root_parser, args, remaining_args):
    root_parser.print_help()


def jpipe_main(argv=None):
    if argv is None:
        argv = sys.argv

    root_parser = argparse.ArgumentParser(
        prog=os.path.basename(argv[0]),
        add_help=False,
    )
    root_parser.set_defaults(func=jpipe_command_callback)

    subparsers = root_parser.add_subparsers()

    for entry_point in importlib_metadata.entry_points()["console_scripts"]:
        if not entry_point.value.startswith("jpipe."):
            continue
        if not entry_point.name.startswith("jpipe-"):
            continue

        subcommand = entry_point.name.partition("jpipe-")[-1]
        entry_point_func = load_entrypoint(entry_point)
        subparser_kwargs = dict(
            add_help=False,
            help=entry_point_func.__description__,
        )

        ep_subparser = subparsers.add_parser(subcommand, **subparser_kwargs)
        ep_subparser.set_defaults(
            func=functools.partial(
                jpipe_subcommand_callback, subcommand, entry_point_func
            )
        )

    args, remaining_args = root_parser.parse_known_args(args=argv[1:])
    args.func(root_parser, args, remaining_args)


if __name__ == "__main__":
    sys.exit(jpipe_main(argv=sys.argv))
