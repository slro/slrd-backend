# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD base exception classes.

This module defines main types of exceptions raised in SLRD project. The base
class SLRDException indicates that the exception is related to SLRD program and
was a result of program-specific causes.

SLRDRuntimeException is a base class for exceptions that happen due to a
dynimic input from a user or is a result of certain external factors. This type
of exceptions should be caught and handled properly to provide a verbose
explanation of the causes (bubble up to user interface etc).

SLRDImplementationError is a base class for exceptions that are a result of an
improper usage of SLRD internal modules (controllers etc.). This type of
exceptions should not happen at all thus should not be caught or processed in
any way except for ensuring graceful shutdown in extreme occasions.

Classes:
    - SLRDException
    - SLRDRuntimeException
    - SLRDImplementationError
"""


class SLRDException(Exception):
    """Base exceptions class.

    Pass an already formatted exception message to its parent class to be
    printed out to STDOUT.
    """

    def __init__(self, msg):
        """Initialization method.

        :param msg: message to print when being raised
        :type msg:  str
        """
        super().__init__(msg)


class SLRDRuntimeException(SLRDException):
    """Base external input related exception class."""


class SLRDImplementationError(SLRDException):
    """Base internal error related exception class.

    In other words the error is critical and is a result of improper usage of
    internal modules. Should not be caught and generally should not happen at
    all. Think of it as a some kind of assertion.
    """
