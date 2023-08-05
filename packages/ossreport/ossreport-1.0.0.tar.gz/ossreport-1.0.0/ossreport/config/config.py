# -*- coding: utf-8 -*-

import json
import os
import yaml


class ConfigFile:
    APIVERSION = "apiVersion"
    KIND = "kind"
    METADATA = "metadata"
    SPEC = "spec"


class MetaData:
    NAME = "name"


class ConfigException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Config(object):
    def __init__(self):
        self._config_file = None
        self._license_file = None
        self._output_file = None
        self._scanoss_file = None

    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ConfigException("config invalid")
        name = name.strip()
        if not name.endswith(".yml") and not name.endswith(".yaml"):
            raise ConfigException("suffix invalid")
        if not os.path.exists(name):
            raise ConfigException("%s not found" % name)
        with open(name) as file:
            self._config_file = yaml.load(file, Loader=yaml.FullLoader)
        if self._config_file is None:
            raise ConfigException("config invalid")

    @property
    def license_file(self):
        return self._license_file

    @license_file.setter
    def license_file(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ConfigException("config invalid")
        name = name.strip()
        if not name.endswith(".json"):
            raise ConfigException("suffix invalid")
        if not os.path.exists(name):
            raise ConfigException("%s not found" % name)
        with open(name, encoding="utf-8") as file:
            self._license_file = json.load(file)
        if self._license_file is None:
            raise ConfigException("config invalid")

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, name):
        if not isinstance(name, str):
            raise ConfigException("output invalid")
        name = name.strip()
        if len(name) != 0:
            if not name.endswith(".pdf") and not name.endswith(".xlsx"):
                raise ConfigException("suffix invalid")
            if os.path.exists(name):
                raise ConfigException("%s already exist" % name)
        self._output_file = name

    @property
    def scanoss_file(self):
        return self._scanoss_file

    @scanoss_file.setter
    def scanoss_file(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ConfigException("config invalid")
        name = name.strip()
        if not name.endswith(".json"):
            raise ConfigException("suffix invalid")
        if not os.path.exists(name):
            raise ConfigException("%s not found" % name)
        with open(name, encoding="utf-8") as file:
            self._scanoss_file = json.load(file)
        if self._scanoss_file is None:
            raise ConfigException("config invalid")
