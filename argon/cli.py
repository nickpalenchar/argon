"""
argon - Generate projects from custom templates

Usage:
    argon new <name> [<dir>]
    argon list
"""
import docopt
import sys
import signal
from . import argon
from . import errors


def handle_sigint(h, frame):
    print('')
    sys.exit(1)


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    args = docopt.docopt(__doc__)
    print(args)
    sys.exit(execute_command(args) or 0)


def execute_command(args):
    command = getattr(argon, sys.argv[1], None)
    if args['new']:
        try:
            argon.new(args)
        except errors.BaseException as e:
            return argon_error_messages(e)


def argon_error_messages(exception):
    if type(exception) == errors.TemplateNotFound:
        print(exception)
        print('(use `argon list` for available templates)')
        return 1
