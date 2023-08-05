# -*- coding: utf-8 -*-

from ossreport.proto.proto import Risk, Level, Component, File


class BuilderException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Builder(object):
    _COMPONENT_SEP = ","
    _VULNERABILITIES_SEP = "/"

    _SOURCE_MATCHES = "Matches"

    def __init__(self, scanoss, analyzer):
        self._scanoss = scanoss
        self._analyzer = analyzer

    def _build_risks(self, data):
        def _build_license_risk(data):
            critical, high, medium, low, none = 0, 0, 0, 0, 0
            for component in data:
                for license in component[Component.LICENSE].split(self._COMPONENT_SEP):
                    level = license.split(" ")[0]
                    if level == Level.CRITICAL[0].upper():
                        critical += 1
                    elif level == Level.HIGH[0].upper():
                        high += 1
                    elif level == Level.MEDIUM[0].upper():
                        medium += 1
                    elif level == Level.LOW[0].upper():
                        low += 1
                    elif level == Level.NONE[0].upper():
                        none += 1
            return {
                Risk.__name__.capitalize(): Risk.LICENSE_RISK,
                Level.CRITICAL: critical,
                Level.HIGH: high,
                Level.MEDIUM: medium,
                Level.LOW: low,
                Level.NONE: none,
            }

        def _build_operational_risk(data):
            critical, high, medium, low, none = 0, 0, 0, 0, 0
            # TODO
            return {
                Risk.__name__.capitalize(): Risk.OPERATIONAL_RISK,
                Level.CRITICAL: critical,
                Level.HIGH: high,
                Level.MEDIUM: medium,
                Level.LOW: low,
                Level.NONE: none,
            }

        def _build_security_risk(data):
            critical, high, medium, low, none = 0, 0, 0, 0, 0
            for item in data:
                c, h, m, l, n = item[Component.SECURITY_RISK].split(" ")
                if int(c.lstrip(Level.CRITICAL[0].upper())) > 0:
                    critical += 1
                if int(h.lstrip(Level.HIGH[0].upper())) > 0:
                    high += 1
                if int(m.lstrip(Level.MEDIUM[0].upper())) > 0:
                    medium += 1
                if int(l.lstrip(Level.LOW[0].upper())) > 0:
                    low += 1
                if int(n.lstrip(Level.NONE[0].upper())) > 0:
                    none += 1
            return {
                Risk.__name__.capitalize(): Risk.SECURITY_RISK,
                Level.CRITICAL: critical,
                Level.HIGH: high,
                Level.MEDIUM: medium,
                Level.LOW: low,
                Level.NONE: none,
            }

        return {
            Risk.__name__: [
                _build_license_risk(data),
                _build_operational_risk(data),
                _build_security_risk(data),
            ]
        }

    def _build_components(self, data):
        def _fetch(data):
            critical, high, medium, low, none = 0, 0, 0, 0, 0
            for item in data[File.VULNERABILITIES].split(" "):
                severity = item.split(self._VULNERABILITIES_SEP)[-1].upper()
                if severity == Level.CRITICAL.upper():
                    critical += 1
                elif severity == Level.HIGH.upper():
                    high += 1
                elif severity == Level.MEDIUM.upper():
                    medium += 1
                elif severity == Level.LOW.upper():
                    low += 1
                else:
                    none += 1
            return {
                Component.COMPONENT: " ".join(
                    [data[File.COMPONENT].capitalize(), data[File.VERSION]]
                ),
                Component.SOURCE: " ".join(["1", self._SOURCE_MATCHES]),
                Component.MATCH_TYPE: data[File.ID].capitalize(),
                Component.USAGE: "",
                Component.LICENSE: " ".join(
                    [
                        self._analyzer.license_risk(data[File.LICENSES])[0].upper(),
                        data[File.LICENSES],
                    ]
                ),
                Component.SECURITY_RISK: " ".join(
                    [
                        Level.CRITICAL[0].upper() + str(critical),
                        Level.HIGH[0].upper() + str(high),
                        Level.MEDIUM[0].upper() + str(medium),
                        Level.LOW[0].upper() + str(low),
                        Level.NONE[0].upper() + str(none),
                    ]
                ),
                Component.OPERATIONAL_RISK: "",
            }

        def _update(data, new):
            data[Component.SOURCE] = " ".join(
                [
                    str(
                        int(data[Component.SOURCE].split(" ")[0])
                        + int(new[Component.SOURCE].split(" ")[0])
                    ),
                    self._SOURCE_MATCHES,
                ]
            )
            data[Component.MATCH_TYPE] = (
                data[Component.MATCH_TYPE]
                if new[Component.MATCH_TYPE] in data[Component.MATCH_TYPE]
                else self._COMPONENT_SEP.join(
                    [data[Component.MATCH_TYPE], new[Component.MATCH_TYPE]]
                )
            )
            data[Component.USAGE] = (
                data[Component.USAGE]
                if new[Component.USAGE] in data[Component.USAGE]
                else self._COMPONENT_SEP.join(
                    [data[Component.USAGE], new[Component.USAGE]]
                )
            )
            data[Component.LICENSE] = (
                data[Component.LICENSE]
                if new[Component.LICENSE] in data[Component.LICENSE]
                else self._COMPONENT_SEP.join(
                    [data[Component.LICENSE], new[Component.LICENSE]]
                )
            )
            c, h, m, l, n = new[Component.SECURITY_RISK].split(" ")
            critical, high, medium, low, none = data[Component.SECURITY_RISK].split(" ")
            critical = Level.CRITICAL[0].upper() + str(
                int(critical.lstrip(Level.CRITICAL[0].upper()))
                + int(c.lstrip(Level.CRITICAL[0].upper()))
            )
            high = Level.HIGH[0].upper() + str(
                int(high.lstrip(Level.HIGH[0].upper()))
                + int(h.lstrip(Level.HIGH[0].upper()))
            )
            medium = Level.MEDIUM[0].upper() + str(
                int(medium.lstrip(Level.MEDIUM[0].upper()))
                + int(m.lstrip(Level.MEDIUM[0].upper()))
            )
            low = Level.LOW[0].upper() + str(
                int(low.lstrip(Level.LOW[0].upper()))
                + int(l.lstrip(Level.LOW[0].upper()))
            )
            none = Level.NONE[0].upper() + str(
                int(none.lstrip(Level.NONE[0].upper()))
                + int(n.lstrip(Level.NONE[0].upper()))
            )
            data[Component.SECURITY_RISK] = " ".join(
                [critical, high, medium, low, none]
            )
            data[Component.OPERATIONAL_RISK] = (
                data[Component.OPERATIONAL_RISK]
                if new[Component.OPERATIONAL_RISK] in data[Component.OPERATIONAL_RISK]
                else self._COMPONENT_SEP.join(
                    [data[Component.OPERATIONAL_RISK], new[Component.OPERATIONAL_RISK]]
                )
            )
            return data

        buf = {}
        for item in data:
            b = _fetch(item)
            if b[Component.COMPONENT] not in buf.keys():
                buf[b[Component.COMPONENT]] = b
            else:
                buf[b[Component.COMPONENT]] = _update(buf[b[Component.COMPONENT]], b)
        return {Component.__name__: [v for v in buf.values()]}

    def _build_files(self):
        buf = {File.__name__: []}
        for key, val in self._scanoss.items():
            for v in val:
                if v["id"] == "none":
                    continue
                buf[File.__name__].append(
                    {
                        File.ID: v["id"],
                        File.NAME: key,
                        File.LINES: v["lines"],
                        File.OSS_LINES: v["oss_lines"],
                        File.MATCHED: v["matched"],
                        File.PURL: " ".join([p for p in v["purl"]]),
                        File.VENDOR: v["vendor"],
                        File.COMPONENT: v["component"],
                        File.VERSION: v["version"],
                        File.LATEST: v["latest"],
                        File.URL: v["url"],
                        File.RELEASE_DATE: v["release_date"],
                        File.FILE: v["file"],
                        File.DEPENDENCIES: " ".join([d for d in v["dependencies"]]),
                        File.LICENSES: " ".join([lic["name"] for lic in v["licenses"]]),
                        File.VULNERABILITIES: " ".join(
                            [
                                vul["CVE"] + self._VULNERABILITIES_SEP + vul["severity"]
                                for vul in v["vulnerabilities"]
                            ]
                        ),
                    }
                )
        return buf

    def run(self):
        files = self._build_files()
        components = self._build_components(files[File.__name__])
        risks = self._build_risks(components[Component.__name__])
        return risks, components, files
