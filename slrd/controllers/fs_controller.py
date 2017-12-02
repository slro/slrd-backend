# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Write and read files from a file system.

This module provides an interface to read, write and modify files from/to a
file system.

Todo:
    - finish docstrings
    - implement methods
"""
import logging
from os import makedirs
from os.path import isdir, isfile, islink, exists
from slrd.exceptions.common_exceptions import SLRDIllegalArgumentError
from slrd.exceptions.controller_exceptions import SLRDFSCtrlCreateException, \
                                                  SLRDFSCtrlRmException
from slrd import comlogstr
from shutil import rmtree


class FSController(object):
    """Read, write and modify files in a file system."""

    LOGSTR_MKDIR = 'created directory: %s, mode: %s'
    LOGSTR_MKDIR_MODE_ERR = 'can\'t cast mode argument to integer: %s'
    LOGSTR_SYML_ATK_SUS = 'platform do not support fd-based functions: ' + \
                          'symlink attack is possible'

    ERRMSG_MKDIR_ERR = 'failed to create directory: %s with mode %s: %s'
    ERRMSG_DELDIR_ERR = 'failed to remote subtree: %s: %s'
    ERRMSG_DELDIR_NDIR = 'failed to remove subtree: %s: not a directory'

    def __init__(self):
        """Initialization method."""
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.logger.debug(comlogstr.LOG_INIT_END)

    def __it_exists(self, path, check_func):
        """Implementation of *_exists functions.

        :param path:       path to check an existence of
        :param check_func: function to check with

        :type path:       str
        :type check_func: function

        :return: result of a check
        :rtype:  bool
        """
        result = check_func(path)
        self.logger.debug(comlogstr.LOG_CHECK_RESULT %
                          (check_func.__name__ + '(%s)' % path, result))
        return result

    def file_exists(self, path):
        """Check whether a file exists.

        :param path:         path to a file to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool
        """
        return self.__it_exists(path, isfile)

    def dir_exists(self, path):
        """Check whether a directory exists.

        :param path:         path to a directory to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool
        """
        return self.__it_exists(path, isdir)

    def link_exists(self, path):
        """Check whether a link exists.

        :param path:         path to a link to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool
        """
        return self.__it_exists(path, islink)

    def it_exists(self, path):
        """Check whether path exists.

        :param path:         path to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool
        """
        return self.__it_exists(path, exists)

    def create_dir(self, path, mode):
        """Create a directory.

        :param path: path to a directory to create
        :param mode: permissions with which to create a directory (in *nix
                     format, like 0700)

        :type path: str
        :type mode: str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlCreateException
        """
        try:
            makedirs(path, int(mode, 8))
        except ValueError as e:
            # would fail again if mode is not string
            # (though everything went bananas anyway)
            self.logger.critical(self.LOGSTR_MKDIR_MODE_ERR % mode)
            raise SLRDIllegalArgumentError(e)
        except OSError as e:
            errmsg = self.ERRMSG_MKDIR_ERR % (path, mode, e)
            self.logger.error(self.errmsg)
            raise SLRDFSCtrlCreateException(errmsg)
        self.logger.info(self.LOGSTR_MKDIR % (path, mode))

    def delete_dir(self, path):
        """Delete a directory.

        Remove the directory with all files in it (force, best-effort).

        If directory do not exist the operation considered to be successful. If
        an input path leads to something that is not a directory the exception
        will be raised.

        :param path: path to a directory to delete
        :type path:  str

        :raises: slrd.exceptions.controller_exceptions.SLRDFSCtrlRmException
        """
        if self.dir_exists(path):
            if not rmtree.avoids_symlink_attacks:
                self.logger.warning(self.LOGSTR_SYML_ATK_SUS)
            try:
                rmtree(path)
            # flake8 complains that PermissionError do not exist but
            # I do not want to register on GitLab to submit an issue
            except (OSError, PermissionError) as e:
                errmsg = self.ERRMSG_DELDIR_ERR % (path, e)
                self.logger.error(errmsg)
                raise SLRDFSCtrlRmException(errmsg)
        elif self.it_exists(path):
            errmsg = self.ERRMSG_DELDIR_NDIR % path
            self.logger.error(errmsg)
            raise SLRDFSCtrlCreateException(errmsg)

    def read_file(self, path):
        """."""
        # TODO: implement

    def delete_file(self, path):
        """."""
        # TODO: implement

    def write_to_file(self, data, path, timestamp, force=False):
        """Write data to a file located at a specified path.

        Data is written NOT in a binary mode.

        """
        # TODO: implement

    def check_mode(self, path):
        """."""
        # TODO: implement

    def match_mode_subtree(self, path, dir_mode, other_mode, fd_content=True):
        """."""
        # TODO: implement
