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

import subprocess


class ENScript(object):
    # https://dev.evernote.com/doc/articles/enscript.php

    def __init__(self, enscript, username=None, password=None, database=None):
        self._enscript = enscript
        self._username = username
        self._password = password
        self._database = database

    def _call_enscript(self, *args):
        args = ('wine', self._enscript) + args
        stdout = subprocess.check_output(args=args)
        return stdout

    def createNote(self, content, notebook, title,
                   tags=None, attachments=None, date=None):
        raise NotImplementedError()

    def importNotes(self, enex_file, notebook):
        raise NotImplementedError()

    def showNotes(self, query='any:'):
        raise NotImplementedError()

    def printNotes(self, query='any:'):
        raise NotImplementedError()

    def exportNotes(self, query='any:', enex_file):
        try:
            self._call_enscript('exportNotes', '/q', query, '/f', enex_file)
        except subprocess.CalledProcessError:
            # No results.
            pass

    def createNotebook(self, notebook, type=None):
        raise NotImplementedError()

    def listNotebooks(self, type=None):
        stdout = self._call_enscript('listNotebooks')
        notebooks = [line.strip() for line in stdout.strip().split('\n')]
        return notebooks

    def syncDatabase(self, log_file=None):
        self._call_enscript('syncDatabase')