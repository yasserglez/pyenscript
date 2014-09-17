# -*- coding: utf-8 -*-

import os

from setuptools import setup


src_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(src_dir, 'README.txt')) as f:
    long_description = f.read()

setup(
    name='PyENScript',
    version='0.1.0',
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