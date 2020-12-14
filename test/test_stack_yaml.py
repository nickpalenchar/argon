import unittest
import subprocess
import os
from testutils import test_environment, cat_file


class TestStackConfig(unittest.TestCase):
    """
    the optional stack.yaml file in a stack can alter the beheivor of the cli, including what gets printed,
    and how values are handled.
    """

    def test_yaml_description(self):
        with test_environment('0') as workdir:
            out = subprocess.run(('argon', 'list'), stdout=subprocess.PIPE)
            print(out.stdout)
            self.assertTrue(out.stdout.startswith(b'templatedefs'), msg=out.stdout)
            self.assertIn('the description defined in stack.yaml', out.stdout.decode('utf-8'))

            subprocess.run(('argon', 'new', 'templatedefs', workdir.name, '--values', 'somevalue=YAY'))
            self.assertEqual(cat_file(os.path.join(workdir.name, 'output.txt')),
                             """YAY""")


if __name__ == '__main__':
    unittest.main()
