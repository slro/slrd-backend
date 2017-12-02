# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""."""
import logging
from slrd.strings import comlogstr
from slrd.controllers import fsctrl

# bundle in slrd.exceptions.__init__.py and import in a single line
from slrd.exceptions.controller_exceptions import SLRDFSCtrlCreateException
from slrd.exceptions.manager_exceptions import SLRDBaseDirAllocationError


# NOTE: TODO: might be a good idea to refactor to DataManager
class ConfigManager(object):
    """."""

    DEF_CONFIG = {}  # TODO: what should be there?

    ERRMSG_BDIR_NOT_DIR = 'base directory path should be a directory: %s'
    ERRMSG_BDIR_CRERROR = 'failed to create a base directory: %s'

    LOGSTR_BDIR_NFOUND = 'no base directory detected; creating a fresh one'
    LOGSTR_BDIR_NDIR = 'base directory is not a directory; can\'t proceed'

    def __init__(self, base_dir='~/.slrd/', base_dir_mode='0700'):
        """Initialization method.

        :param base_dir:      path to a directory that should be a data
                              storage root
        :param base_dir_mode: permissions mode to create a base directory with
                              (*nix style like '0700')

        :type base_dir:      str
        :type base_dir_mode: str

        :raise: slrd.exceptions.controller_exceptions.SLRDFSCtrlCreateException
                slrd.exceptions.manager_exceptions.SLRDFSBaseDirAllocationError
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.base_dir = base_dir
        self.base_dir_mode = base_dir_mode
        if not fsctrl.it_exists(base_dir):
            try:
                self.logger.info(self.LOGSTR_BDIR_NFOUND)
                fsctrl.create_dir(self.base_dir, self.base_dir_mode)
            except SLRDFSCtrlCreateException as e:
                raise SLRDBaseDirAllocationError(
                        self.ERRMSG_BDIR_CRERROR % e)
        # path exists but not a directory
        elif not fsctrl.dir_exists(base_dir):
            self.logger.critical(self.LOGSTR_BDIR_NDIR)
            raise SLRDBaseDirAllocationError(
                    self.ERRMSG_BDIR_NOT_DIR % base_dir)
        elif # TODO: check mode of a directory; assert match self.base_dir_mode
        # TODO: put SLRD config file there or locate an existing one
        self.logger.debug(comlogstr.LOG_INIT_END)
