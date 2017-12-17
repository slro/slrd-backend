# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Test slrd.utils.type_checker module."""
import logging
from os.path import isfile
import unittest
from slrd.exceptions import SLRDIllegalArgumentError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# NOTE: importing TypeChecker singletone after initalizing logger to
# see its initialization logs (they need a root logger to be visible)
from slrd.utils import type_checker as tc


class TestFSController(unittest.TestCase):
    """Test slrd.controllers.fs_controller module.

    All test cases are somehow connected with a file system and test files will
    be spawned in the same folder where this test module is located.
    """

    def test_default_mode(self):
        """Test whether type checker is initalized in STRICT mode."""
        self.assertEqual(tc.mode, 0)

    def test_set_mode(self):
        """Test setting check mode."""
        modes = {
            'NEXIST': False,
            42: False,
            ('tuple', 'this', 'is'): False,
            'STRICT': True,
            'NOCHECK': True,
        }
        for mode, exists in modes.items():
            with self.subTest(mode=mode):
                if exists:
                    tc.set_mode(mode)
                    self.assertEqual(
                            tc.mode,
                            tc.__class__.TYPE_CHECK_MODES.index(mode)
                            )
                else:
                    with self.assertRaises(SLRDIllegalArgumentError):
                        tc.set_mode(mode)

    def test_check_types(self):
        """Test actual type checker functionality."""
        args = {
            (str, 42): False,
            (int, 'integer'): False,
            (str, int, 42, 43): False,
            (str, callable, isfile, open): False,
            (str, 'this is string'): True,
            (str, str, 'str1', 'str2'): True,
            (int, str, 42, 'string'): True,
            (open, callable): True,
            (str, int, callable, 'str', 43, isfile): True,
        }
        comp_args = [(dict, {}), (list, []), (tuple, ()), (set, set())]
        for argset, passes in args.items():
            with self.subTest(argset=argset):
                if not passes:
                    with self.assertRaises(SLRDIllegalArgumentError):
                        tc.check_types(*argset)
        # nothing should be raised
        for comp_arg in comp_args:
            tc.check_types(*comp_arg)
