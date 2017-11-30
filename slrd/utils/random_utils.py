# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Utility functions that deal with randomness.

This module provides various utility functions that utilize randomness: random
string generator, random timestamp generator etc.

Classes:
    - RandomUtils

Todo:
    - finish docstrings
    - implement methods
"""
import logging


class RandomUtils(object):
    """Randomness-related utility functions."""

    def __init__(self):
        """."""
        self.logger = logging.getLogger(__name__)
        self.logger.debug("initialization started")
        self.logger.debug("initialization finished")

    def get_random_string(self, length):
        """."""

    def get_random_datetime(self, formt, lbound=None, rbound=None):
        """."""
