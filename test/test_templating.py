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

    def test_renders_value_in_many_files(self):
        with test_environment() as workdir:
            subprocess.run(('argon', 'new', 'onevalmanyfiles', workdir.name, '--values',
                            'global=Nick,alias=my_precious'))

            tests = (('file1.txt', 'This line, also known as my_precious, ends with Nick.'),
                     ('file2.txt', 'This line has Nick in the middle.'),
                     ('file3.txt', 'Nick is at the start of this line.'))

            for filename, expect in tests:
                with self.subTest(key=filename):
                    self.assertEqual(cat_file(os.path.join(workdir.name, filename)), expect)


    def test_renders_value_in_directory(self):
        pass


if __name__ == '__main__':
    unittest.main()