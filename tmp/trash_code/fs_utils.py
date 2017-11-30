# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Utility functions to assist with file system related checks.

This module includes FSUtils class that simplifies checks for file existence
and other FS-related checks.

Classes:
    - FSUtils

Todo:
    -
"""
import logging
from os.path import exists, isfile, isdir, islink


class FSUtils(object):
    """File system related utility functions (checks mostly)."""

    def __init__(self):
        """Initialization method.

        Nothing here except for a logger instance initialization.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("initialization started")
        self.logger.debug("initialization finished")

    def __it_exists(self, path, check_func, except_class, except_msg):
        """Implementation of *_exists functions.

        Input parameters are inherited from the *_exists classes.
        """
        if not check_func(path):
            self.logger.warning("existence check failed: %s" % path)
            raise except_class(except_msg)
        self.logger.info("existence check passed")

    def file_exists(self, path, except_class, except_msg):
        """Check whether a file exists.

        :param path:         path to a file to check an existence of
        :param except_class: exception class to raise in case the file do not
                             exist
        :param except_msg:   message to pass to the exception class when
                             raising it

        :type path:          str
        :type except_class:  child of Exception class
        :type except_msg:    str

        :raise: except_class
        """
        self.__it_exists(path, isfile, except_class, except_msg)
        self.logger.debug("passed parameters to __it_exists() function")

    def dir_exists(self, path, except_class, except_msg):
        """Check whether a directory exists.

        :param path:         path to a directory to check an existence of
        :param except_class: exception class to raise in case the directory do
                             not exist
        :param except_msg:   message to pass to the exception class when
                             raising it

        :type path:          str
        :type except_class:  child of Exception class
        :type except_msg:    str

        :raise: except_class
        """
        self.__it_exists(path, isdir, except_class, except_msg)
        self.logger.debug("passed parameters to __it_exists() function")

    def link_exists(self, path, except_class, except_msg):
        """Check whether a link exists.

        :param path:         path to a link to check an existence of
        :param except_class: exception class to raise in case the link do not
                             exist
        :param except_msg:   message to pass to the exception class when
                             raising it

        :type path:          str
        :type except_class:  child of Exception class
        :type except_msg:    str

        :raise: except_class
        """
        self.__it_exists(path, islink, except_class, except_msg)
        self.logger.debug("passed parameters to __it_exists() function")

    def it_exists(self, path, except_class, except_msg):
        """Check whether path exists.

        :param path:         path to check an existence of
        :param except_class: exception class to raise in case the path do not
                             exist
        :param except_msg:   message to pass to the exception class when
                             raising it

        :type path:          str
        :type except_class:  child of Exception class
        :type except_msg:    str

        :raise: except_class
        """
        self.__it_exists(path, exists, except_class, except_msg)
        self.logger.debug("passed parameters to __it_exists() function")
