#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="gregory_online",
    description="Online watching HTTP server of ROOT on port 9009",
    author="me",
    author_email="jaromrax@gmail.com",
    license="GPL2",
    version=get_version("gregory_online/version.py"),
    packages=['gregory_online'],
    package_data={'gregory_online': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/gregory_online'],
    install_requires = ['fire','scipy','pyfromroot','pytermgui','readchar','fastnumbers','sshkeyboard','terminaltables'],
)
