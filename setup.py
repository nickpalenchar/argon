from setuptools import find_packages, setup
from argon import __VERSION__

with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

setup(
    name='argon',
    version=__VERSION__,
    description='My new cli',
    long_description='My new cli',
    url='https://github.com/nickpalenchar/argon', # TODO: add a url here
    author='Nick Palenchar',
    author_email='',
    license='',
    classifiers=[], # see https://pypi.org/classifiers/ for valid classifiers
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'argon=argon.cli:main'
        ]
    }
)
