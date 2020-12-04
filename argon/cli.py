"""
argon - Generate projects from custom templates

Usage:
    argon new <name> [--values <keyvalues>] [<dir>]
    argon list

Options
    --values    Supply key=value pairs to be used with a template, separated by commas.
                e.g. foo=bar,baz=quix
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
    sys.exit(execute_command(args) or 0)


def execute_command(args):
    command = getattr(argon, sys.argv[1], None)
    try:
        command(args)
    except errors.BaseException as e:
        return argon_error_messages(e)


def argon_error_messages(exception):
    if type(exception) == errors.TemplateNotFound:
        print(exception)
        print('(use `argon list` for available templates)')
        return 1
