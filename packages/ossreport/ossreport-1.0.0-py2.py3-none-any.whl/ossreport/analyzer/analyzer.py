# -*- coding: utf-8 -*-

from ossreport.proto.proto import Level


class AnalyzerException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Analyzer(object):
    def __init__(self, config, license):
        pass

    def license_risk(self, data):
        # TODO
        return Level.NONE

    def operational_risk(self, data):
        # TODO
        return Level.NONE
