"""
Keep track of values the user gets. A place to parse, get, and prompt/update.

"""

class InvalidStringValue(Exception):
    pass


class Values:
    
    def __init__(self, **values):
        self._values = {}

    def __dict__(self):
        return self._values

    def __getitem__(self, value):
        return self._values[value]

    def parse_string(self, string):
        key, value = string.split('=', maxsplit=1)
        self._values[key] = value

    def parse_strings(self, strings):
        for string in strings:
            self.parse_string(string)

    def prompt(self, key):
        value = input(f'Enter a value for {key}:\n> ')
        self._values[key] = value


if __name__ == '__main__':
    import sys
    values = Values()
    values.parse_strings(sys.argv[1:])
    print((values))

