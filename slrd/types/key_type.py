# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""SLRD key data type module.

Todo:
    - docs
    - implement
"""
from super_type import SuperType


class KeyType(SuperType):
    """SLRD key data type.

    This data type stores references to corresponding value files.
    """

    def __init__(self, raw_yaml=None, **kwargs):
        """Initialization method.

        :param raw_yaml:
        :param kwargs:

        :type raw_yaml:
        :type kwargs:

        :raise: <???>
        """
