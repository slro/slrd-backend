# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Git repository controller."""
import logging
from slrd.strings import comlogstr


class GPGController(object):
    """."""

    def __init__(self):
        """."""
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        # init stuff goes here
        self.logger.debug(comlogstr.LOG_INIT_END)
