# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD controllers exception classes.

This module defines SLRD exceptions and errors that are raised in SLRD
controllers (precisely, in slrd.controllers.* modules).

Classes:
    -
"""
from slrd.exceptions import SLRDRuntimeException, SLRDImplementationError


class SLRDFSCtrlCreateException(SLRDRuntimeException):
    """SLRD file system controller creation error.

    For instance, FS controller failed to create a file in a system (folder,
    link etc).
    """


class SLRDFSCtrlRmException(SLRDRuntimeException):
    """SLRD file system controller failed to remote file(s)."""
