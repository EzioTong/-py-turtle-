Signal-triggered process reloader
=================================

Pyexec allows to setup signal handler, which will reload current process. This
functionality might be used to restart application, e.g. when the code’s been
changed, by sending an appropriate signal to the python process.

Exemplary usage:
----------------

.. code:: python

    import os
    import pyexec
    import signal
    import sys

    def handler():
        sys.stderr.write('Reloading process!\n')
        return sys.argv + ['reloaded']

    sys.stderr.write('[%d]: argv: %r\n' % (os.getpid(), sys.argv))
    pyexec.install(signal.SIGUSR1, handler)
    signal.pause()

The output from the python process after sending the USR1 signal twice:

::

    $ python example.py
    [20785]: argv: ['example.py']
    Reloading process!
    [20785]: argv: ['example.py', 'reloaded']
    Reloading process!
    [20785]: argv: ['example.py', 'reloaded', 'reloaded']


