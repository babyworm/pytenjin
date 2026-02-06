##
## Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com)
## License: MIT License
##

"""Command-line interface for PyTenjin template engine."""

import argparse
import json
import sys

import tenjin
from tenjin.helpers import *  # noqa: F401,F403


def main(args=None):
    parser = argparse.ArgumentParser(
        prog="pytenjin",
        description="PyTenjin - a fast and full-featured template engine based on embedded Python.",
    )
    parser.add_argument(
        "--version", action="version", version="pytenjin %s" % tenjin.__version__
    )

    subparsers = parser.add_subparsers(dest="command")

    # render subcommand
    render_parser = subparsers.add_parser("render", help="Render a template file")
    render_parser.add_argument("template", help="Template file path to render")
    render_parser.add_argument(
        "-c", "--context", help="JSON file path for context data", default=None
    )
    render_parser.add_argument(
        "-o", "--output", help="Output file path (default: stdout)", default=None
    )

    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help()
        return 0

    if parsed.command == "render":
        return _do_render(parsed)

    return 0


def _do_render(parsed):
    context = {}
    if parsed.context:
        try:
            with open(parsed.context, "r") as f:
                context = json.load(f)
        except (IOError, OSError) as e:
            sys.stderr.write("Error reading context file: %s\n" % e)
            return 1
        except ValueError as e:
            sys.stderr.write("Error parsing JSON context: %s\n" % e)
            return 1

    try:
        engine = tenjin.Engine()
        output = engine.render(parsed.template, context)
    except Exception as e:
        sys.stderr.write("Error rendering template: %s\n" % e)
        return 1

    if parsed.output:
        try:
            with open(parsed.output, "w") as f:
                f.write(output)
        except (IOError, OSError) as e:
            sys.stderr.write("Error writing output file: %s\n" % e)
            return 1
    else:
        sys.stdout.write(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
