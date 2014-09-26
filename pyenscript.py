# -*- coding: utf-8 -*-
#
# Copyright 2014 Yasser Gonzalez Fernandez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
PyENScript: a Python wrapper for the Evernote ENScript.exe executable.
"""

import os
import sys
import subprocess


class ENScript(object):
    """ENScript.exe wrapper.

    Calls the Evernote ENScript.exe executable using the subprocess module.
    See https://dev.evernote.com/doc/articles/enscript.php for the API
    documentation.
    """

    def __init__(self, enscript, username=None, password=None, database=None,
                 suppress_output=False):
        if sys.version_info[0] == 3:
            string_types = (str, bytes)  # subprocess also checks for bytes
        else:
            string_types = basestring
        if isinstance(enscript, string_types):
            self._base_args = [enscript]
        else:
            self._base_args = list(enscript)
        if username:
            self._base_args.extend(['/u', username])
        if password:
            self._base_args.extend(['/p', password])
        if database:
            self._base_args.extend(['/d', database])
        self._suppress_output = suppress_output

    def _execute_enscript(self, extra_args):
        args = self._base_args + extra_args
        if self._suppress_output:
            with open(os.devnull, 'w') as devnull:
                subprocess.call(args, stdout=devnull, stderr=devnull)
        else:
            subprocess.call(args)

    def createNote(self, content, notebook, title,
                   tags=None, attachments=None, date=None):
        raise NotImplementedError()

    def importNotes(self, enex_file, notebook):
        raise NotImplementedError()

    def showNotes(self, query='any:'):
        raise NotImplementedError()

    def printNotes(self, query='any:'):
        raise NotImplementedError()

    def exportNotes(self, enex_file, query='any:'):
        try:
            self._execute_enscript(['exportNotes', '/q', query, '/f', enex_file])
        except subprocess.CalledProcessError:
            # No results.
            pass

    def createNotebook(self, notebook, type=None):
        raise NotImplementedError()

    def listNotebooks(self, type=None):
        stdout = self._execute_enscript(['listNotebooks'])
        notebooks = [line.strip() for line in stdout.strip().split('\n')]
        return notebooks

    def syncDatabase(self, log_file=None):
        self._execute_enscript(['syncDatabase'])