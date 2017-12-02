# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""."""
from slrd.exceptions import SLRDRuntimeException, SLRDImplementationError


class SLRDBaseDirAllocationError(SLRDRuntimeException):
    """SLRD failed to allocate a base directory for storing a data."""
