# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD exception classes

Classes:
    - SLRDException
"""


class SLRDException(Exception):
    """Base exceptions class.

    Passed an already formatted exception message to its parent class to be
    printed out to STDOUT.
    """

    def __init__(self, msg):
        """Initialization method.

        :param msg: message to print when being raised
        :type msg:  str
        """
        super(type(self), self).__init__(msg)


class SLRDFSBaseDirAllocationError(SLRDException):
    """SLRD failed to allocate a base directory for storing a data."""
