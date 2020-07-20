'''
Created on 04/08/2014

@author: julia
'''
import sys
from outputstream_wrapper import OutputStreamWrapper


class BasicUserIO(object):
    """Class to bypass output and input"""

    def __init__(self, ins=sys.stdin, out=None):
        '''
        Params:
            ins: input stream
            out: output stream, should have write method
        '''
        self._ins = ins
        if not out:
            out = OutputStreamWrapper(sys.stdout)
        self._out = out

    @property
    def out(self):
        """Get output stream"""
        return self._out

    @property
    def ins(self):
        """Get input stream"""
        return self._ins
