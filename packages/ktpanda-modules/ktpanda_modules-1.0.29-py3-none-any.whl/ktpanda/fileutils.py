# fileutils.py
#
# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
fileutils
=========

Simple utilities for dealing with files / directories.
'''

import os
import json
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Union

@contextmanager
def _save_file(path:Path, **kw):
    '''Save a file to path, creating a temporary file while writing, then atomically replacing'''

    tf = tempfile.NamedTemporaryFile(
        dir=str(path.parent), prefix=path.name,
        suffix='.write-temp', delete=False, **kw)

    ok = False
    try:
        with tf:
            yield tf

        os.replace(tf.name, path)
        ok = True
    finally:
        if not ok:
            try:
                os.unlink(tf.name)
            except OSError:
                pass

def save_file(path:Path, data:Optional[Union[str, bytes]]=None, **kw):
    '''Writes `data` to a path, first writing to a temporary file, then atomically
    replacing the destination. If `data` is a `bytes` object, the file is opened in binary
    mode. If `data` is a `str`, the file is opened as text, with the default encoding of
    `"utf8"`. If `data` is None, then a context manager is returned allowing the file to
    be incrementally written. Extra keyword arguments are passed to
    `tempfile.NamedTemporaryFile`.'''

    if isinstance(data, bytes):
        with _save_file(path, **kw) as fp:
            fp.write(data)
    elif isinstance(data, str):
        kw.setdefault('mode', 'w')
        kw.setdefault('encoding', 'utf8')
        with _save_file(path, **kw) as fp:
            fp.write(data)
    else:
        return _save_file(path, **kw)

def save_json(path:Path, data:Union[dict | list], indent=4):
    '''Write `data` (a JSON object) to `path` using `save_file`.'''
    with save_file(path, mode='w', encoding='utf8') as fp:
        json.dump(data, fp, indent=indent)

def load_json(path:Path, default=None, **kw):
    '''Load JSON from the given path, returning `default` if the file does not exist.'''
    try:
        with path.open('r', encoding='utf8') as fp:
            return json.load(fp, **kw)
    except FileNotFoundError:
        return default
