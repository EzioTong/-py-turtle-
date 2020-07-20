# pyexec.py
# Copyright (c) 2015-2017 Arkadiusz Bokowy
#
# This file is a part of pyexec.
#
# This project is licensed under the terms of the MIT license.

import sys
from os import execl
from signal import signal


# NOTE: Changing this number will alter package version as well.
__version__ = '1.1.1'


def _handler(signum, stack):
    argv = _handler.callback()
    if argv is None:
        argv = sys.argv
    execl(sys.executable, sys.executable, *argv)


def install(signum, callback=lambda: None):
    """Install pyexec functionality for the given signal number.

    Optionally, one can specify a callback function, which will be called
    before the process is reloaded. In this function one can perform some
    shutdown routines, e.g. saving data. This callback function also gives
    a possibility to alter process command line arguments by returning the
    list with new ones. Otherwise, the sys.argv will be used.

    Note:
        This function is not thread-safe. It should be called in the main
        thread - only the main thread is allowed to set signal handler.

    Arguments:
        signum: The signal number for which the exec handler is installed.
        callback: Function called just before the exec action.

    Returns:
        Previously installed handler (if any) for the given signal number.

    """
    _handler.callback = callback
    return signal(signum, _handler)
