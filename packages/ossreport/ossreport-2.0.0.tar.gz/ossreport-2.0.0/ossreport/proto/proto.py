# -*- coding: utf-8 -*-


class Risk:
    LICENSE_RISK = "License Risk"
    OPERATIONAL_RISK = "Operational Risk"
    SECURITY_RISK = "Security Risk"


class Level:
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"


class Component:
    COMPONENT = "Component"
    SOURCE = "Source"
    MATCH_TYPE = "Match Type"
    USAGE = "Usage"
    LICENSE = "License"
    SECURITY_RISK = "Security Risk"
    OPERATIONAL_RISK = "Operational Risk"


class File:
    ID = "ID"
    NAME = "Name"
    LINES = "Lines"
    OSS_LINES = "OSS Lines"
    MATCHED = "Matched"
    PURL = "PKG URL"
    VENDOR = "Vendor"
    COMPONENT = "Component"
    VERSION = "Version"
    LATEST = "Latest"
    URL = "URL"
    RELEASE_DATE = "Release Date"
    FILE = "File"
    DEPENDENCIES = "Dependencies"
    LICENSES = "Licenses"
    VULNERABILITIES = "Vulnerabilities"
