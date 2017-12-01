# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Write and read data files from a file system.

This module provides an interface to read, write and modify data files from/to
a file system.

Todo:
    - finish docstrings
    - implement methods
"""
import logging
from os import makedirs
from os.path import isdir, exists
from slrd import comlogstr
from slrd import SLRDFSBaseDirAllocationError


# NOTE: (ddnomad)
# > not sure we need this to be a class
# > base_dir should be stored in settings/conf manager class
# > and fs_controller do not care where to through files (read etc)
# > so there is no need to store any state altogether
class FSController(object):
    """Read, write and modify data files in a file system."""

    # would be very grateful if somebody formulated it in a less dumb way
    ERRMSG_BDIR_NOT_DIR = "base directory path should be a directory: %s"
    ERRMSG_BDIR_CRERROR = "failed to create a base directory: %s"

    def __init__(self, base_dir='~/.slrd/'):
        """Initialization method.

        :param base_dir: path to a directory that should be a data storage root
        :type base_dir: str

        :raise: <???>
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)

        if not exists(base_dir):
            try:
                # slightly not optimized move to increase verbosity
                makedirs(base_dir, int('0700', 8))
            except OSError as e:
                raise SLRDFSBaseDirAllocationError(
                        self.ERRMSG_BDIR_CRERROR % e)
        elif not isdir(base_dir):
            raise SLRDFSBaseDirAllocationError(
                    self.ERRMSG_BDIR_NOT_DIR % base_dir)

        self.base_dir = base_dir
        self.logger.debug(comlogstr.LOG_INIT_END)

    def write_to_file(self, data, path, timestamp, force=False):
        """Write data to a file located at a specified path.

        Data is written NOT in a binary mode.

        """

    def read_file(self, path):
        """."""

# NOTE (ddnomad)
# > I'm not sure we need this method as it can be done in one line anyway.
# > See __init__ from this class for an example
#     def check_file_exists(self, path):
#         """ """

    def delete_file(self, path):
        """."""

    def create_dir(self, path):
        """."""

    def delete_dir(self, path):
        """."""
