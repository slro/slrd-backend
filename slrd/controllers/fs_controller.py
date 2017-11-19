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


class FSController(object):
    """Read, write and modify files in a file system."""

    def __init__(self, base_dir='~/.slrd/'):
        """Initialization method.

        :param base_dir: path to a directory that should be a data storage root
        :type base_dir: str

        :raise: <???>
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("initialization started")

        self.base_dir = base_dir

        self.logger.debug("initialization finished")

    def write_to_file(self, data, path, timestamp, force=False):
        """Write data to a file located at a specified path.

        Data is written NOT in binary mode.

        """

    def read_file(self, path):
        """ """

    def check_file_exists(self, path):
        """ """

    def delete_file(self, path):
        """ """

    def create_dir(self, path):
        """ """

    def delete_dir(self, path):
        """ """
