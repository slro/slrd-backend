# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD controllers exception classes.

This module defines SLRD exceptions and errors that are raised in SLRD
controllers (precisely, in slrd.controllers.* modules).

Classes:
    - SLRDFSCtrlCreateException
    - SLRDFSCtrlRmException
    - SLRDFSCtrlReadException
"""
from slrd.exceptions import SLRDRuntimeException, SLRDImplementationError


class SLRDFSCtrlCreateException(SLRDRuntimeException):
    """SLRD file system controller creation error.

    For instance, FS controller failed to create a file in a system (folder,
    link etc).
    """


class SLRDFSCtrlRmException(SLRDRuntimeException):
    """SLRD file system controller failed to remote file(s)."""


class SLRDFSCtrlReadException(SLRDRuntimeException):
    """SLRD file system controller failed to read a file."""


class SLRDFSCtrlWriteException(XOPOSRuntimeException):
    """XOPOS file system controller failed to write to a file."""
