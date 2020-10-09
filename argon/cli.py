"""
argon - Generate projects from custom templates

Usage:
    argon new <name> [<dir>]
    argon list
"""
import docopt
import sys
from . import argon
from . import errors


def main():
    args = docopt.docopt(__doc__)
    print(args)
    sys.exit(execute_command(args) or 0)


def execute_command(args):
    if args['new']:
        try:
            argon.new(args['<name>'], args['<dir>'] or '.')
        except errors.BaseException as e:
            return argon_error_messages(e)


def argon_error_messages(exception):
    if type(exception) == errors.TemplateNotFound:
        print(exception)
        print('(use `argon list` for available templates)')
        return 1
