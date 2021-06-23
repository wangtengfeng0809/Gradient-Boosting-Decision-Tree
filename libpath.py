# coding: utf-8
"""Find the path to xgboost dynamic library files."""

import os
import platform
from typing import List
import sys


class XGBoostLibraryNotFound(Exception):

def find_lib_path() -> List[str]:

    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    dll_path = [
        # normal, after installation `lib` is copied into Python package tree.
        os.path.join(curr_path, 'lib'),
        # editable installation, no copying is performed.
        os.path.join(curr_path, os.path.pardir, os.path.pardir, 'lib'),
        # use libxgboost from a system prefix, if available.  This should be the last
        # option.
        os.path.join(sys.prefix, 'lib'),
    ]

    if sys.platform == 'win32':
        if platform.architecture()[0] == '64bit':
            dll_path.append(
                os.path.join(curr_path, '../../windows/x64/Release/'))
            # hack for pip installation when copy all parent source
            # directory here
            dll_path.append(os.path.join(curr_path, './windows/x64/Release/'))
        else:
            dll_path.append(os.path.join(curr_path, '../../windows/Release/'))
            # hack for pip installation when copy all parent source
            # directory here
            dll_path.append(os.path.join(curr_path, './windows/Release/'))
        dll_path = [os.path.join(p, 'xgboost.dll') for p in dll_path]
    elif sys.platform.startswith('linux') or sys.platform.startswith(
            'freebsd'):
        dll_path = [os.path.join(p, 'libxgboost.so') for p in dll_path]
    elif sys.platform == 'darwin':
        dll_path = [os.path.join(p, 'libxgboost.dylib') for p in dll_path]
    elif sys.platform == 'cygwin':
        dll_path = [os.path.join(p, 'cygxgboost.dll') for p in dll_path]

    lib_path = [p for p in dll_path if os.path.exists(p) and os.path.isfile(p)]

