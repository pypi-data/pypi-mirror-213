import sys
from importlib import import_module
from pathlib import Path

from ..constants import PROVIDERS
from ..providers import brettops


def build_command(parser, args):
    if not Path(args.filename).exists():
        parser.error(f"file not found: {args.filename}")

    pipeline = brettops.load(args.filename)
    output_format = import_module(f".{args.output_format}", "cici.providers")
    output_format.dump(pipeline, sys.stdout)


def build_parser(subparsers):
    parser = subparsers.add_parser(
        "build", help="build BrettOps CI file into target format"
    )
    parser.add_argument("filename", nargs="?", default=".brettops-pipeline.yml")
    parser.add_argument(
        "-t",
        "--to",
        dest="output_format",
        choices=PROVIDERS,
        default="brettops",
        help="output format [brettops]",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="DIR",
        dest="output_path",
        type=Path,
        default=Path.cwd().absolute(),
    )
    parser.set_defaults(func=build_command)
    return parser
