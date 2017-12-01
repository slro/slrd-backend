# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD base exception classes.

This module defines main types of exceptions raised in SLRD project. The base
class SLRDException indicates that the exception is related to SLRD program and
was a result of program-specific causes.

SLRDRuntimeException is a base class for exceptions that happen due to a
dynimic input from the user or is a result of external factors. This type of
exceptions should be caught and handled properly to provide a verbose
explanation of the causes.

SLRDImplementationError is a base class for exceptions that are a result of an
improper usage of SLRD internal modules (controllers etc.). This type of
exceptions should not happen at all thus should not be caught or processed in
any way except for ensuring graceful shutdown in an extreme occasions.

Classes:
    - SLRDException
    - SLRDRuntimeException
    - SLRDImplementationError
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
