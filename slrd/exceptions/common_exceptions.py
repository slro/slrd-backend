# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD exceptions that are shared between all packages.

Classes:
    - SLRDIllegalArgumentError
"""
from slrd.exceptions import SLRDRuntimeException, SLRDImplementationError


class SLRDIllegalArgumentError(SLRDImplementationError):
    """Illegal argument was passed to a function/method."""
