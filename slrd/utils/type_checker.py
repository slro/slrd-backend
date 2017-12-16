# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Utility module that provides a type check functionality.

Prefered way of using it: create a singletone instance in a root __init__.py of
a project; import in each module where type check is needed and then call it
any function/method like that:

```
import slrd.typechecker as tc  # instantized in __init__.py

    def func(arg1, arg2, arg3):
        # make sure it's the first call
        tc.check_types(str, str, int, **locals())
```

Todo:
    - implement + docs
"""
import logging
from slrd.exceptions import SLRDIllegalArgumentError
from slrd.strings import comlogstr


class TypeChecker(object):
    """Class capable of performing type checks."""

    TYPE_CHECK_MODES = [
            'STRICT',  # do all type checking work
            'NOCHECK'  # bypass all calls doing nothing
            ]

    LOGSTR_MODESET = 'mode set: %s'
    LOGSTR_TC_CALLED = 'performing type check [mode: %s]'
    LOGSTR_TC_SKIP = 'skipping type check [mode: %s]'
    ERRSTR_UNSUP_MODE = 'unsupported mode: %s'
    ERRSTR_TCLEN_ODD = 'amount of input parameters have to be even: got %i'
    ERRSTR_CHECK_FAIL = 'type check failed for: %s is %s'

    def __init__(self, mode):
        """Initialization method.

        :param mode: mode of operation of a type checker. For a possible modes
                     please see self.TYPE_CHECK_MODES list.
        :type mode:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.mode = 0  # default to STRICT mode
        self.set_mode(mode)
        self.mode_verb = self.TYPE_CHECK_MODES[self.mode]
        self.logger.debug(comlogstr.LOG_INIT_END)

    def set_mode(self, mode):
        """Set type checker mode.

        :param mode: mode of operation of a type checker. For a possible modes
                     please see self.TYPE_CHECK_MODES list.
        :type mode:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        try:
            self.mode = self.TYPE_CHECK_MODES.index(mode)
        except ValueError:
            errstr = self.ERRSTR_UNSUP_MODE % str(mode)
            self.logger.critical(errstr)
            raise SLRDIllegalArgumentError(errstr)
        self.logger.info(self.LOGSTR_MODESET % mode)

    def check_types(self, *args):
        """Check types of input arguments.

        Input parameters are passed one by one: first required types are
        passed, then arguments to check for types. Check is performed for
        respective pairs (i, n/2 + i), where n - even number of input passed to
        this function, i in [0, n/2).

        An exception will be raised if at least one check has failed.z

        Instead of type a callable object (i.e. function) can be passed that
        should return bool value when called on a corresponding argument. If
        returned value is truthy check is considered to be passed.

        For example, type check for a function should look like this:

        ```
        check_types(open, callable)  # cause callable(<func>) will return True
        ```

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        if self.mode == 0:
            self.logger.info(
                    self.LOGSTR_TC_CALLED % self.mode_verb)
            args_len = len(args)
            if not args_len % 2:
                errmsg = self.ERRSTR_TCLEN_ODD % args_len
                self.logger.critical(errmsg)
                raise SLRDIllegalArgumentError(errmsg)
            for i in range(args_len):
                arg = args[args_len + i]
                ttype = args[i]
                if callable(ttype):
                    check_res = ttype(arg)
                else:
                    check_res = isinstance(arg, ttype)
                if not check_res:
                    errmsg = self.ERRSTR_CHECK_FAIL % (str(arg), str(ttype))
                    self.logger.critical(errmsg)
                    raise SLRDIllegalArgumentError(errmsg)
            return
        self.logger.debug(self.LOGSTR_TC_SKIP % self.mode_verb)
