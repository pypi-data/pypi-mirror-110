#!/usr/bin/env python

from sfinx.version import __version__ as version
import argparse


class CliTool(object):
    __version__ = version

    def __init__(self, *args, **kwargs):
        parser = self._get_argparser()
        self.args = parser.parse_args()

        if self.args.action.lower() == "version":
            print("version: %s" % version)
            return

    @staticmethod
    def _get_argparser():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="action")
        subparsers.required = True
        subparsers.add_parser("version", help="Print the version")
        return parser


def main():
    CliTool()


if __name__ == "__main__":
    main()
