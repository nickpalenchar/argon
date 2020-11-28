import os
import yaml
from collections import ChainMap

BUNDLES = ('bundle.yml', 'bundle.yaml')

class InvalidBundle(Exception):
    """Raised when bundle.yml is missing or invalid"""
    pass


class Bundle:

    def __init__(self, workdir):
        config = ChainMap(self._parse_yaml(workdir), self._get_defaults(workdir))
        self.name = config['name']
        self.values = config['values']

    def __repr__(self):
        return self.name

    def _get_defaults(self, workdir):
        return {
            'name': workdir.split(os.sep)[-1],
            'values': []
        }

    def _parse_yaml(self, workdir):
        for b in BUNDLES:
            yaml_file = os.path.join(workdir, b)
            try:
                with open(yaml_file) as fh:
                    bundle_config = yaml.safe_load(fh.read()) or {}

                    return bundle_config
            except FileNotFoundError:
                pass
        raise InvalidBundle(f'Bundle at {workdir} has no bundle.yml file')
