"""
Sets up a temporary environment with different config for testing argon cli commands
"""
import os
import shutil
import yaml
from tempfile import TemporaryDirectory
from contextlib import contextmanager
ARGON_CONFIG = 'ARGON_CONFIG'


@contextmanager
def test_environment():
    old_environ = os.environ.get(ARGON_CONFIG)
    config_dir = TemporaryDirectory()
    bundles_dir = TemporaryDirectory()
    argon_config = {
        'argonPath': [bundles_dir.name]
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
        yield bundles_dir, config_dir
    finally:
        config_dir.cleanup()
        bundles_dir.cleanup()
        if old_environ:
            os.environ[ARGON_CONFIG] = old_environ
        else:
            del os.environ[ARGON_CONFIG]

def main():
    with test_environment() as dirs:
        print(dirs)
        breakpoint()
        pass
        # breakpoint()
    pass



if __name__ == '__main__':
    main()