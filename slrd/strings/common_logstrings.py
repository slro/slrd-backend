# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Common logging strings definition module

Provide logging strings to other classes to use while allowing for changes
being made in a single place.

Classes:
    - CommonLogstrings

Todo:
    -
"""


class CommonLogstrings(object):
    """Common logging strings."""

    # Should be logged in __init__ method of each class. LOG_INIT_START should
    # be called on instance creation (first line of __init__) and LOG_INIT_END
    # should be called as a last line in the initialization method. Preferred
    # logging level is DEBUG.
    LOG_INIT_START = "initialization started"
    LOG_INIT_END = "initialization finished"

    # Should be logged when some kind of a check was made. Prefered log level
    # depends on an importance of a check but generally DEBUG is a good start.
    LOG_CHECK_RESULT = "check %s result: %s"
