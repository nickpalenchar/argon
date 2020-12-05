import os
import sys
import shutil
import re
from values import Values
from argon.config import Config
from argon.errors import FileExistsError
from argon.stack_parsing import Bundle, InvalidBundle
import logging
from argon.errors import *
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('ARGON_LOGLEVEL', 'WARNING'))


# SRC = '/usr/local/templates'
TEMPLATE_SRC = 'src' # name of the directory to look for within a template bundle
WORKDIR = '/tmp/argon-tmp'
CONFIG = Config()


def new(args):

    def parse_custom_values(s):
        result = {}
        values = [v for v in s.split(',') if v]
        for pair in values:
            try:
                key, val = pair.split('=')
                result[key] = val
            except ValueError:
                print('--values got an invalid format. Wants key=value pairs, separated by ,')
                sys.exit(1)
        return result

    name = args['<name>']
    dest = args['<dir>'] or '.'
    values = args['--values'] or ''
    """Create new template. To be used by cli.py"""
    try:
        pre_main()
        main(name, Values(**parse_custom_values(values)), dest=dest)
    except KeyboardInterrupt:
        shutil.rmtree(os.path.join(WORKDIR, name))


def list(args):
    """
    :param args:
    :return:
    """
    bundles = []

    for p in CONFIG.argonPath:
        for filename in os.listdir(p):
            try:
                bundle = Bundle(os.path.join(p, filename))
                bundles.append(bundle.fmtstr())

            except InvalidBundle:
                pass
    if not bundles:
        print('(no stacks found)')

    print('\n'.join(bundles))
    return


def pre_main():
    """Remove old workdirs before starting"""
    try:
        shutil.rmtree(os.path.join(WORKDIR))
    except (OSError, FileNotFoundError) as e:
        pass


def main(name, user_values, workdir=WORKDIR, dest=''):
    template_bundle = get_template_bundle(name)
    ensure_valid_bundle(template_bundle)
    render_from_template(template_bundle, workdir, user_values)
    move_contents_to_destination(workdir, dest)


def move_contents_to_destination(start, dest):
    for file in os.listdir(start):
        try:
            shutil.move(os.path.join(start, file), dest)
        except shutil.Error as e:
            raise FileExistsError(e.args[0])


def ensure_valid_bundle(template_bundle):
    if TEMPLATE_SRC not in os.listdir(template_bundle):
        raise TemplateBundleError(f'Missing required directory "{TEMPLATE_SRC}" in bundle')


def render_from_template(template_bundle, dest, user_values):
    cwd = os.getcwd()
    abs_src = os.path.join(cwd, template_bundle, TEMPLATE_SRC)
    abs_dest = os.path.join(cwd, dest)
    shutil.copytree(abs_src, abs_dest)
    os.chmod(dest, 0o777)
    for oldname, newname in reversed(get_files_to_rename(dest, user_values)):
        os.rename(oldname, newname)

    for dirpath, _, filenames in os.walk(dest):
        for filename in filenames:
            try:
                render_file(os.path.join(dirpath, filename), user_values)
            except MissingRequiredValue as e:
                print(f'Cannot render file {os.path.join(dirpath, filename)}: missing required template value')
                raise e


def render_file(filepath, user_values: Values):
    """
    Replaces template values in a file, *overwritting the original**.
    """
    new_text = []
    with open(filepath, 'r') as fh:
        for line in iter(fh.readline, ''):
            new_text.append(render_str(line, user_values))

    with open(filepath, 'w') as fh:
        fh.writelines(new_text)


def get_files_to_rename(tree, user_values: Values):
    """Returns a list of 2-tuple strings containing the file source and what it should be renamed to.

    This runs for both files AND directories
    """
    to_rename = []
    for dirpath, dirnames, filenames in os.walk(tree):
        for dirname in dirnames:
            newname = render_str(dirname, user_values)
            if newname != dirname:
                to_rename.append((os.path.join(dirpath, dirname), os.path.join(dirpath, newname)))
        for filename in filenames:
            newname = render_str(filename, user_values)
            if newname != filename:
                to_rename.append((filename, newname))
    return to_rename


def render_str(string, user_values: Values):
    def replacer(match):
        key = match.groups()[0].strip()
        if key not in user_values._values:
            user_values.prompt(key)
        return user_values[key]

    return re.sub('<%\s*([^(%>)]*\s*)%>', replacer, string, count=0)


def get_template_bundle(template_name):
    for path in CONFIG.argonPath:
        template_bundle = find_template_bundle(os.path.expandvars(path), template_name)
        if template_bundle:
            return template_bundle
    raise TemplateNotFound(f'No template with name {template_name} found!')


def find_template_bundle(src, template_name):
    try:
        template_path = os.path.join(src, template_name)
        os.stat(template_path)
    except FileNotFoundError:
        return None
    return template_path


def copy_within_dir(dirpath, dest):
    for f in os.listdir(dirpath):
        pass #TODO copy everything


if __name__ == '__main__':
    name = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else '.'
    new(name, dest)


