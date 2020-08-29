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
        print('oh it was this one?')
        print(e)


def main(name):
    src = get_template_source(name)
    render_from_template(src, WORKDIR, **{'name': 'mason'})


def render_from_template(src, dest, **values):
    shutil.copytree(src, dest)
    os.chmod(dest, 0o777)
    for dirpath, dirnames, filenames in os.walk(dest):
        print([render_str(dirname, **values) for dirname in dirnames])
        


def render_str(string, **values):
    def replacer(match):
        value = match.groups()[0]
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

