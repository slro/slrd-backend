"""."""

import logging
from slrd.exceptions.base_exceptions import *
from slrd.exceptions.controller_exceptions import *
from slrd.exceptions.common_exceptions import *
from slrd.exceptions.manager_exceptions import *


# bundle exceptions for specific modules to import them in a single line
class FSControllerExceptions(object):
    """Encapsulate all exceptions used in slrd.controllers.fs_controller."""

    def __init__(self):
        """Initialization method."""
        self.SLRDIllegalArgumentError = SLRDIllegalArgumentError
        self.SLRDFSCtrlCreateException = SLRDFSCtrlCreateException
        self.SLRDFSCtrlRmException = SLRDFSCtrlRmException
        self.SLRDFSCtrlReadException = SLRDFSCtrlReadException


logging.getLogger(__name__).addHandler(logging.NullHandler())
fsctrl_exceptions = FSControllerExceptions()
