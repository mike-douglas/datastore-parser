from distutils.core import setup
from setuptools import find_packages

readme = ''
dependencies = []

with open('README.md') as r:
    readme = r.read()

with open('requirements.txt') as r:
    dependencies = r.readlines()

setup(
    name='Datastore Parser',
    version='1.0.0',
    description='Parser for Lua data produced by Altoholic Addon for World of Warcraft',
    long_description=readme,

    author='Mike Douglas',
    author_email='michael.j.douglas@gmail.com',

    url='https://github.com/mike-douglas/datastore_parser',

    packages=find_packages(),

    install_requires=dependencies,
)
