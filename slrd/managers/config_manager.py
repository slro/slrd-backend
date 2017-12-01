# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""."""
import logging
from slrd import comlogstr
from slrd.controllers import fsctrl


class ConfigManager(object):
    """."""

    DEF_CONF = {
            'base_dir_mode': '0700'
    }

    ERRMSG_BDIR_NOT_DIR = "base directory path should be a directory: %s"
    ERRMSG_BDIR_CRERROR = "failed to create a base directory: %s"

    def __init__(self, base_dir='~/.slrd/'):
        """Initialization method.

        :param base_dir: path to a directory that should be a data storage root
        :type base_dir:  str

        :raise: <???>
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.base_dir = base_dir
        
        if not fsctrl.it_exists(base_dir):
            try:
                # slightly not optimized move to increase verbosity
                makedirs(base_dir, int('0700', 8))
            except OSError as e:
                raise SLRDFSBaseDirAllocationError(
                        self.ERRMSG_BDIR_CRERROR % e)
        elif not isdir(base_dir):
            raise SLRDFSBaseDirAllocationError(
                    self.ERRMSG_BDIR_NOT_DIR % base_dir)

        self.logger.debug(comlogstr.LOG_INIT_END)
