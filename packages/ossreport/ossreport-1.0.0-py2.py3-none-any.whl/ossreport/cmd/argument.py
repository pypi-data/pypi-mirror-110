# -*- coding: utf-8 -*-

import argparse
import os

from ossreport.__version__ import __version__


class Argument(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="SCANOSS Report")
        self._add()

    def _add(self):
        self._parser.add_argument(
            "--config-file",
            action="store",
            default=os.path.join(os.getcwd(), "config", "config.yml"),
            dest="config_file",
            help="config file (default: %s)"
            % os.path.join("ossreport", "config", "config.yml"),
            required=False,
        )
        self._parser.add_argument(
            "--license-file",
            action="store",
            default=os.path.join(os.getcwd(), "data", "license.json"),
            dest="license_file",
            help="license file (default: %s)"
            % os.path.join("ossreport", "data", "license.json"),
            required=False,
        )
        self._parser.add_argument(
            "--output-file",
            action="store",
            dest="output_file",
            help="output file (.pdf|.xlsx)",
            required=True,
        )
        self._parser.add_argument(
            "--scanoss-file",
            action="store",
            dest="scanoss_file",
            help="scanoss file (.json)",
            required=True,
        )
        self._parser.add_argument(
            "-v", "--version", action="version", version=__version__
        )

    def parse(self, argv):
        return self._parser.parse_args(argv[1:])
