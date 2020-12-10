import unittest
import subprocess
import os
from testutils import test_environment, cat_file


class TestArgon(unittest.TestCase):

    def test_renders_value_in_file(self):
        with test_environment() as workdir:
            subprocess.run(('argon', 'new', 'singlevalue', workdir.name, '--values', 'myvalue=HELLO'))
            self.assertEqual(cat_file(os.path.join(workdir.name, 'hello.txt')),
                             """Hello, this contains one value, it is HELLO.""")

    def test_renders_multiple_values_in_file(self):
        with test_environment() as workdir:
            subprocess.run(('argon', 'new', 'multivalue', workdir.name, '--values',
                            'first=fee,second=fi,third=fo,fourth=fum'))
            self.assertEqual(cat_file(os.path.join(workdir.name, 'hola.txt')),
                             """The giant says: fee, fi, fo, fum!""")


    def test_renders_value_in_directory(self):
        pass

if __name__ == '__main__':
    unittest.main()