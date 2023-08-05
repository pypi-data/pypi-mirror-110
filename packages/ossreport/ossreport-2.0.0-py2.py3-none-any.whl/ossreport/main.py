# -*- coding: utf-8 -*-

import sys

from ossreport.analyzer.analyzer import Analyzer, AnalyzerException
from ossreport.builder.builder import Builder, BuilderException
from ossreport.cmd.argument import Argument
from ossreport.cmd.banner import BANNER
from ossreport.config.config import Config, ConfigException
from ossreport.logger.logger import Logger
from ossreport.printer.printer import Printer, PrinterException


def main():
    print(BANNER)

    argument = Argument()
    arg = argument.parse(sys.argv)

    try:
        config = Config()
        config.config_file = arg.config_file
        config.license_file = arg.license_file
        config.output_file = arg.output_file
        config.scanoss_file = arg.scanoss_file
    except ConfigException as e:
        Logger.error(str(e))
        return -1

    Logger.info("report running")

    try:
        analyzer = Analyzer(config.config_file, config.license_file)
    except AnalyzerException as e:
        Logger.error(str(e))
        return -2

    try:
        builder = Builder(config.scanoss_file, analyzer)
        risks, components, files = builder.run()
    except BuilderException as e:
        Logger.error(str(e))
        return -3

    try:
        printer = Printer(risks, components, files, config.output_file)
        printer.run()
    except PrinterException as e:
        Logger.error(str(e))
        return -4

    Logger.info("report exiting")

    return 0
