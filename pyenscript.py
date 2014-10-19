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
import tempfile
import subprocess


class ENScript(object):
    """Evernote ENScript.exe wrapper.

    This class calls the Evernote ENScript.exe executable using the
    subprocess module. The API mimics the ENScript.exe arguments documented
    in https://dev.evernote.com/doc/articles/enscript.php.
    """

    def __init__(self, enscript, silence_stderr=False,
                 username=None, password=None, database=None):
        """Initialize the ENScript.exe wrapper.

        enscript must be a string with the path to ENScript.exe (on Windows)
        or a sequence with Wine in the first position and the ENScript.exe path
        in the second position (on GNU/Linux). The stderr output will be
        redirected to /dev/null if silence_stderr is set to True.
        """
        if self._is_string(enscript):
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

    @staticmethod
    def _is_string(value):
        # Check if value is a string (Python 2 and Python 3 compatible).
        if sys.version_info[0] == 3:
            string_types = (str, bytes)  # subprocess also checks for bytes.
        else:
            string_types = basestring
        return isinstance(value, string_types)

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

    def create_note_from_content(self, content, notebook, title, tags=None,
                                 attachments=None, date=None):
        """Create a new note."""
        f = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        f.write(content)
        f.close()  # Close file first so it can be opened on Windows.
        self.create_note_from_filename(f.name, notebook, title, tags,
                                       attachments, date)
        os.unlink(f.name)

    def create_note_from_filename(self, filename, notebook, title, tags=None,
                                  attachments=None, date=None):
        """Create a new note."""
        extra_args = ['createNote', '/s', filename, '/n', notebook, '/i', title]
        for option, argument in (('/t', tags), ('/a', attachments)):
            if argument:
                if self._is_string(argument):
                    extra_args.extend([option, argument])
                else:
                    for value in argument:
                        extra_args.extend([option, value])
        if date:
            extra_args.extend(['/c', date])
        self._call_enscript(extra_args)

    def import_notes(self, enex_file, notebook):
        """Import one or more notes from an Evernote export file (ENEX)."""
        extra_args = ['importNotes', '/s', enex_file, '/n', notebook]
        self._call_enscript(extra_args)

    def show_notes(self, query='any:'):
        """Set the current note list view to the results of a query."""
        extra_args = ['showNotes', '/q', query]
        self._call_enscript(extra_args)

    def print_notes(self, query='any:'):
        """Print a set of notes."""
        extra_args = ['printNotes', '/q', query]
        self._call_enscript(extra_args)

    def export_notes(self, enex_file, query='any:'):
        """Export the set of notes to an Evernote export file (ENEX)."""
        extra_args = ['exportNotes', '/q', query, '/f', enex_file]
        self._call_enscript(extra_args)

    def create_notebook(self, notebook, type_=None):
        """Create a new notebook."""
        extra_args = ['createNotebook', '/n', notebook]
        if type_:
            extra_args.extend(['/t', type_])
        self._call_enscript(extra_args)

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
