# -*- coding: utf-8 -*-

from ossreport.config.config import ConfigFile
from ossreport.proto.proto import Level


class AnalyzerException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Analyzer(object):
    _SPEC_RISK = "risk"
    _SPEC_LICENSE = "license"
    _SPEC_CONDITIONS = "conditions"
    _SPEC_LIMITATIONS = "limitations"
    _SPEC_PERMISSIONS = "permissions"

    def __init__(self, config, license):
        if (
            config.get(ConfigFile.SPEC, None) is None
            or config[ConfigFile.SPEC].get(self._SPEC_RISK, None) is None
        ):
            raise AnalyzerException("config invalid")
        self._config = config[ConfigFile.SPEC][self._SPEC_RISK]
        self._license = license

    def license_risk(self, data):
        def _match_license(data):
            buf = None
            for item in self._license["licenses"]:
                if item["licenseId"] == data:
                    buf = item
                    break
            return buf

        def _match_rule(license, rule):
            permissions_matched, conditions_matched, limitations_matched = (
                False,
                False,
                False,
            )
            if (
                license.get(self._SPEC_PERMISSIONS, None) is not None
                and rule.get(self._SPEC_PERMISSIONS, None) is not None
            ):
                permissions_matched = set(rule[self._SPEC_PERMISSIONS]).issubset(
                    set(license[self._SPEC_PERMISSIONS])
                )
            if (
                license.get(self._SPEC_CONDITIONS, None) is not None
                and rule.get(self._SPEC_CONDITIONS, None) is not None
            ):
                conditions_matched = set(rule[self._SPEC_CONDITIONS]).issubset(
                    set(license[self._SPEC_CONDITIONS])
                )
            if (
                license.get(self._SPEC_LIMITATIONS, None) is not None
                and rule.get(self._SPEC_LIMITATIONS, None) is not None
            ):
                limitations_matched = set(rule[self._SPEC_LIMITATIONS]).issubset(
                    set(license[self._SPEC_LIMITATIONS])
                )
            return permissions_matched and conditions_matched and limitations_matched

        if self._config.get(self._SPEC_LICENSE, None) is None:
            raise AnalyzerException("config invalid")
        license = _match_license(data)
        if license is None:
            raise AnalyzerException("license invalid")
        buf = {}
        for key, val in self._config[self._SPEC_LICENSE].items():
            if val is None or len(val) == 0:
                continue
            buf[key] = _match_rule(license, val)
        if (
            buf.get(Level.CRITICAL.lower(), None) is not None
            and buf[Level.CRITICAL.lower()] is True
        ):
            return Level.CRITICAL
        elif (
            buf.get(Level.HIGH.lower(), None) is not None
            and buf[Level.HIGH.lower()] is True
        ):
            return Level.HIGH
        elif (
            buf.get(Level.MEDIUM.lower(), None) is not None
            and buf[Level.MEDIUM.lower()] is True
        ):
            return Level.MEDIUM
        elif (
            buf.get(Level.LOW.lower(), None) is not None
            and buf[Level.LOW.lower()] is True
        ):
            return Level.LOW
        else:
            pass
        return Level.NONE

    def operational_risk(self, data):
        # TODO
        return Level.NONE
