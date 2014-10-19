# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup


src_dir = os.path.abspath(os.path.dirname(__file__))

try:
    # Try to get the latest version string dynamically from git:
    # (latest version, commits since latest release, and commit SHA-1)
    git_args = ['git', '--work-tree', src_dir,
                '--git-dir', os.path.join(src_dir, '.git'), 'describe']
    with open(os.devnull, 'w') as devnull:
        version = subprocess.check_output(git_args, stderr=devnull).strip()
except subprocess.CalledProcessError:
    # Set statically if git repo not available
    version = '0.1.0'

with open(os.path.join(src_dir, 'README.txt')) as f:
    long_description = f.read()

setup(name='PyENScript',
      version=version,
      description='A Python wrapper for the Evernote ENScript.exe executable',
      long_description=long_description,
      url='https://github.com/yglezfdez/pyenscript',
      author='Yasser Gonzalez Fernandez',
      author_email='contact@yglezfdez.com',
      license='Apache License Version 2.0',
      py_modules=['pyenscript'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)