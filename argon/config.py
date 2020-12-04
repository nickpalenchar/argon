"""
Singleton config object represents the various configuration settings available in argon. Initialization handles
logic for determining what set of config to load.
"""

import os
import yaml
from collections import namedtuple
import logging
log = logging.getLogger('argon')

DEFAULT_CONFIG = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '.argonconfig.yaml'
)
VALID_CONFIG_FIELDS = ('argonPath',)
ARGON_CONFIG_OVERRIDE = os.environ.get('ARGON_CONFIG')

configValues = namedtuple('ConfigValues', VALID_CONFIG_FIELDS)


def get_config():
    return os.environ.get('ARGON_CONFIG')


class Config:

    CONFIG_PATH_MACOS = '$HOME/.argonconfig.yaml'

    def __init__(self):
        if ARGON_PATH := get_config() and os.path.exists(os.path.expandvars(get_config())):
            values = self.get_values_from_file(get_config())
            log.info('Loaded custom config from environment variable $ARGON_CONFIG')
        elif os.path.exists(os.path.expandvars(self.CONFIG_PATH_MACOS)):
            values = self.get_values_from_file(os.path.expandvars(self.CONFIG_PATH_MACOS))
            log.info(f'Loaded custom config file at {self.CONFIG_PATH_MACOS}')
        else:
            values = self.get_values_from_file(DEFAULT_CONFIG)
            log.info('Loaded default argonconfig file')

        self._values = values

    def __getattr__(self, item):
        return self._values[item]

    def get_values_from_file(self, filepath):
        with open(filepath) as fh:
            return yaml.full_load(fh.read())

    def ensure_valid_fields(self, values_dict):
        for key in values_dict.keys():
            if key not in VALID_CONFIG_FIELDS:
                raise ValueError
