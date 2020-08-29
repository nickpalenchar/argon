import os
import sys
import shutil
import re


class MissingRequiredValue(Exception):
    pass


SRC = '/usr/local/templates'
WORKDIR = '/tmp/argon-tmp'


def pre_main(name):
    """Remove old workdirs before starting"""
    try:
        shutil.rmtree(os.path.join(WORKDIR))
    except (OSError, FileNotFoundError) as e:
        pass


def main(name):
    src = get_template_source(name)
    render_from_template(src, WORKDIR, **{'name': 'mason', 'author': 'Nick Palenchar'})


def render_from_template(src, dest, **values):
    shutil.copytree(src, dest)
    os.chmod(dest, 0o777)
    for oldname, newname in reversed(get_files_to_rename(dest, **values)):
        os.rename(oldname, newname)

    for dirpath, _, filenames in os.walk(dest):
        for filename in filenames:
            try:
                render_file(os.path.join(dirpath, filename), **values)
            except MissingRequiredValue as e:
                print(f'Cannot render file {os.path.join(dirpath, filename)}: missing required template value')
                raise e


def render_file(filepath, **values):
    """
    Replaces template values in a file, *overwritting the original**.
    """
    new_text = []
    with open(filepath, 'r') as fh:
        for line in iter(fh.readline, ''):
            new_text.append(render_str(line, **values))

    with open(filepath, 'w') as fh:
        fh.writelines(new_text)


def get_files_to_rename(tree, **values):
    """Returns a list of 2-tuple strings containing the file source and what it should be renamed to.

    This runs for both files AND directories
    """
    to_rename = []
    for dirpath, dirnames, filenames in os.walk(tree):
        for dirname in dirnames:
            newname = render_str(dirname, **values)
            if newname != dirname:
                to_rename.append((os.path.join(dirpath, dirname), os.path.join(dirpath, newname)))
        for filename in filenames:
            newname = render_str(filename, **values)
            if newname != filename:
                to_rename.append((filename, newname))
    return to_rename


def render_str(string, **values):
    def replacer(match):
        value = match.groups()[0].strip()
        if value not in values:
            raise MissingRequiredValue(value)
        return values[value]

    return re.sub('<%\s*([^(%>)]*\s*)%>', replacer, string, count=0)


def get_template_source(template_name):
    template_path = os.path.join(SRC, template_name)
    os.stat(template_path)
    return template_path


if __name__ == '__main__':
    name = sys.argv[1]
    try:
        pre_main(name)
        main(name)
    except KeyboardInterrupt:
        shutil.rmtree(os.path.join(WORKDIR, name))

