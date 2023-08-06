import argparse

from .cli.build import build_parser
from .cli.bundle import bundle_parser
from .cli.update import update_parser


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True)

    build_parser(subparsers=subparsers)
    bundle_parser(subparsers=subparsers)
    update_parser(subparsers=subparsers)

    args = parser.parse_args()
    args.func(parser=parser, args=args)
