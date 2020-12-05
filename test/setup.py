"""
Sets up a temporary environment with different config for testing argon cli commands
"""
import os
import unittest
import shutil
import yaml
import subprocess
from tempfile import TemporaryDirectory
from contextlib import contextmanager
ARGON_CONFIG = 'ARGON_CONFIG'


class TestArgon(unittest.TestCase):

    def test_renders_value_in_file(self):

        with test_environment() as workdir:
            subprocess.run(('argon', 'new', 'singlevalue', workdir.name, '--values', 'myvalue=HELLO'))
            self.assertEqual(cat_file(os.path.join(workdir.name, 'hello.txt')),
                             """Hello, this contains one value, it is HELLO.""")

def cat_file(filepath):
    with open(filepath, 'r') as fh:
        return fh.read()

@contextmanager
def test_environment(stack_dir='default'):
    """
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


def main():
    with test_environment() as dirs:
        S = subprocess.run(('argon', 'list'))
        print(S.stdout)
        pass
        # breakpoint()
    pass



if __name__ == '__main__':
    unittest.main()
