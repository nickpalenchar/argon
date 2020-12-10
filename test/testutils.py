import os
from tempfile import TemporaryDirectory
from contextlib import contextmanager
import shutil
import yaml
ARGON_CONFIG = 'ARGON_CONFIG'


def cat_file(filepath):
    with open(filepath, 'r') as fh:
        return fh.read()


@contextmanager
def test_environment(stack_dir='default'):
    """
    Sets up a temporary environment with different config for testing argon cli commands

    :param stack_dir: the name of the directory within test/templates to add as stacks
    """
    old_environ = os.environ.get(ARGON_CONFIG)
    config_dir = TemporaryDirectory()
    bundles_dir = TemporaryDirectory()
    work_dir = TemporaryDirectory()
    argon_config = {
        'argonPath': [os.path.join(bundles_dir.name, 'templates', stack_dir)]
    }

    argon_config_path = os.path.join(config_dir.name, '.argonconfig.yaml')
    with open(argon_config_path, 'a') as fh:
        fh.write(yaml.safe_dump(argon_config))

    os.environ[ARGON_CONFIG] = os.path.join(argon_config_path)

    source_templates = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates'
    )
    shutil.copytree(source_templates, os.path.join(bundles_dir.name, 'templates'))

    try:
        yield work_dir
    finally:
        config_dir.cleanup()
        bundles_dir.cleanup()
        if old_environ:
            os.environ[ARGON_CONFIG] = old_environ
        else:
            del os.environ[ARGON_CONFIG]

