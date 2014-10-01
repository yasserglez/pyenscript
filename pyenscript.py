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

    def __init__(self, enscript, silence_stderr=False,
                 username=None, password=None, database=None):
        """Initialize the ENScript.exe wrapper.

        enscript must be a string with the path to ENScript.exe (on Windows)
        or a sequence with Wine in the first position and the ENScript.exe path
        in the second position (on GNU/Linux). ENScript.exe's stderr will be
        redirected to /dev/null if silence_stderr is set to True.
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
        self._silence_stderr = silence_stderr

    def _call_enscript(self, extra_args):
        # Call the ENScript.exe executable using subprocess.
        try:
            args = self._base_args + extra_args
            if self._silence_stderr:
                with open(os.devnull, 'w') as devnull:
                    output = subprocess.check_output(args, stderr=devnull)
            else:
                output = subprocess.check_output(args)
        except subprocess.CalledProcessError:
            # Return codes not documented.
            output = None
        return output

    def create_note(self, content, notebook, title,
                    tags=None, attachments=None, date=None):
        """Create a new note."""
        raise NotImplementedError()

    def import_notes(self, enex_file, notebook):
        """Import one or more notes from an Evernote export file (ENEX)."""
        raise NotImplementedError()

    def show_notes(self, query='any:'):
        """Set the current note list view to the results of a query."""
        raise NotImplementedError()

    def print_notes(self, query='any:'):
        """Print a set of notes."""
        raise NotImplementedError()

    def export_notes(self, enex_file, query='any:'):
        """Export the set of notes to an Evernote export file (ENEX)."""
        extra_args = ['exportNotes', '/q', query, '/f', enex_file]
        self._call_enscript(extra_args)

    def create_notebook(self, notebook, type=None):
        """Create a new notebook."""
        raise NotImplementedError()

    def list_notebooks(self, type_=None):
        """Lists existing notebooks."""
        extra_args = ['listNotebooks']
        if type_:
            extra_args.extend(['/t', type_])
        output = self._call_enscript(extra_args)
        notebooks = [line.strip() for line in output.strip().split('\n')]
        return notebooks

    def sync_database(self, log_file=None):
        """Synchronize with the Evernote service."""
        extra_args = ['syncDatabase']
        if log_file:
            extra_args.extend(['/l', log_file])
        self._call_enscript(extra_args)