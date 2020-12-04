"""
The interface for an argon bundle, derived from a directory's containing bundle.yml

bundles should be constructed with the Bundle class, rather than operating on raw contents
"""

import os
import yaml
from collections import ChainMap

STACKS = ('bundle.yml', 'bundle.yaml')

class InvalidBundle(Exception):
    """Raised when bundle.yml is missing or invalid"""
    pass


class Bundle:

    def __init__(self, workdir):
        config = ChainMap(self._parse_yaml(workdir), self._get_defaults(workdir))
        self.name = config['name']
        self.summary = config['summary']
        self.values = config['values']

    def __repr__(self):
        return self.name

    def fmtstr(self):
        """Formats the bundle's name and summary (if exists) to be used with """
        summary = f' - {self.summary}' if self.summary else ''
        return f'{self.name}{summary}'

    def _get_defaults(self, workdir):
        return {
            'name': workdir.split(os.sep)[-1],
            'summary': '',
            'values': []
        }

    def _parse_yaml(self, workdir):
        for b in STACKS:
            yaml_file = os.path.join(workdir, b)
            try:
                with open(yaml_file) as fh:
                    bundle_config = yaml.safe_load(fh.read()) or {}

                    return bundle_config
            except FileNotFoundError:
                pass
        raise InvalidBundle(f'Bundle at {workdir} has no bundle.yml file')