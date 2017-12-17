# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""."""
import logging
from slrd.utils.type_checker import TypeChecker


logging.getLogger(__name__).addHandler(logging.NullHandler())
type_checker = TypeChecker()  # all checks enabled
