# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
###########################################################################
import os
import sys
import subprocess

from textwrap import dedent


try:
    from skbuild import setup
except ImportError:
    print('Please update pip, you need pip 10 or greater,\n'
          ' or you need to install the PEP 518 requirements in pyproject.toml yourself', file=sys.stderr)
    raise

TOP_DIR = os.path.dirname(__file__) or os.getcwd()
PACKAGE_NAME = 'onnxruntime_extensions'


def read_git_refs():
    release_branch = False
    stdout, _ = subprocess.Popen(
            ['git'] + ['log', '-1', '--format=%H'],
            cwd=TOP_DIR,
            stdout=subprocess.PIPE, universal_newlines=True).communicate()
    HEAD = dedent(stdout.splitlines()[0]).strip('\n\r')
    stdout, _ = subprocess.Popen(
            ['git'] + ['show-ref', '--head'],
            cwd=TOP_DIR,
            stdout=subprocess.PIPE, universal_newlines=True).communicate()
    for _ln in stdout.splitlines():
        _ln = dedent(_ln).strip('\n\r')
        if _ln.startswith(HEAD):
            _, _2 = _ln.split(' ')
            if (_2.startswith('refs/remotes/origin/rel-')):
                release_branch = True
    return release_branch, HEAD


def read_requirements():
    with open(os.path.join(TOP_DIR, "requirements.txt"), "r") as f:
        requirements = [_ for _ in [dedent(_) for _ in f.readlines()] if _ is not None]
    return requirements


# read version from the package file.
def read_version():
    version_str = '1.0.0'
    with (open(os.path.join(TOP_DIR, 'onnxruntime_extensions/_version.py'), "r")) as f:
        line = [_ for _ in [dedent(_) for _ in f.readlines()] if _.startswith("__version__")]
        if len(line) > 0:
            version_str = line[0].split('=')[1].strip('" \n\r')

    # is it a dev build or release?
    if os.path.isdir(os.path.join(TOP_DIR, '.git')):
        rel_br, cid = read_git_refs()
        if not rel_br:
            version_str += '+' + cid[:7]
    return version_str


long_description = ''
with open(os.path.join(TOP_DIR, "README.md"), 'r') as f:
    long_description = f.read()
    start_pos = long_description.find('# Introduction')
    start_pos = 0 if start_pos < 0 else start_pos
    end_pos = long_description.find('# Contributing')
    long_description = long_description[start_pos:end_pos]


config = 'Release'
cmake_args = [
    '-DOCOS_ENABLE_PYTHON=ON',
    '-DOCOS_ENABLE_CTEST=OFF',
    '-DCMAKE_BUILD_TYPE=' + config
]


setup(
    name=PACKAGE_NAME,
    version=read_version(),
    description="ONNXRuntime Extensions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Microsoft Corporation',
    author_email='onnx@microsoft.com',
    packages=['onnxruntime_extensions'],
    cmake_install_dir='onnxruntime_extensions',
    cmake_args = cmake_args,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: C++",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: Implementation :: CPython",
        'License :: OSI Approved :: MIT License'
    ],
)
