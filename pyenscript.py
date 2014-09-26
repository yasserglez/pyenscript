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
    """Evernote ENScript.exe executable wrapper.

    Implements a Python wrapper that calls the Evernote ENScript.exe Windows
    executable using the subprocess module. It can be used with Wine on
    GNU/Linux. See https://dev.evernote.com/doc/articles/enscript.php
    for the API documentation.
    """

    def __init__(self, enscript, suppress_output=False, username=None,
                 password=None, database=None):
        """Initialize the ENScript.exe wrapper.

        escript must be a string with the path to ENScript.exe (on Windows)
        or a sequence with Wine in the first position and the ENScript.exe path
        in the second position (on GNU/Linux). ENScript.exe output will be
        redirected to /dev/null if suppress_output is set to True.
        """
        if sys.version_info[0] == 3:
            string_types = (str, bytes)  # subprocess also checks for bytes.
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
        # Call the ENScript.exe executable using subprocess.
        args = self._base_args + extra_args
        if self._suppress_output:
            with open(os.devnull, 'w') as devnull:
                subprocess.call(args, stdout=devnull, stderr=devnull)
        else:
            subprocess.call(args)

    def createNote(self, content, notebook, title,
                   tags=None, attachments=None, date=None):
        """Create a new note."""
        raise NotImplementedError()

    def importNotes(self, enex_file, notebook):
        """Import one or more notes from an Evernote export file (ENEX)."""
        raise NotImplementedError()

    def showNotes(self, query='any:'):
        """Set the current note list view to the results of a query."""
        raise NotImplementedError()

    def printNotes(self, query='any:'):
        """Print a set of notes."""
        raise NotImplementedError()

    def exportNotes(self, enex_file, query='any:'):
        """Export the set of notes to an Evernote export file (ENEX)."""
        try:
            self._execute_enscript(['exportNotes', '/q', query, '/f', enex_file])
        except subprocess.CalledProcessError:
            # No results.
            pass

    def createNotebook(self, notebook, type=None):
        """Create a new notebook."""
        raise NotImplementedError()

    def listNotebooks(self, type=None):
        """Lists existing notebooks."""
        stdout = self._execute_enscript(['listNotebooks'])
        notebooks = [line.strip() for line in stdout.strip().split('\n')]
        return notebooks

    def syncDatabase(self, log_file=None):
        """Synchronize with the Evernote service."""
        self._execute_enscript(['syncDatabase'])