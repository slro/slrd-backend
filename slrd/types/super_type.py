# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Module that provides a unified superclass for all SLRD data types.

Todo:
    - implement?
    - docs?
"""
import yaml


class SuperType(object):
    """Underlying class of all SLRD data types."""

    def __init__(self, raw_yaml=None, **kwargs):
        """Initialization method.

        Enforce that input data is either of two options (not both):
            - raw YAML string that should be loaded
            - keyword arguments that should be resolved by a child

        Then save input data to an instance field for a post-processing by a
        specific child instance.

        :param raw_yaml: raw YAML that should be resolved to arguments for
                         a specific child instance
        :kwargs:         keyword arguments to bypass to a child saving it
                         to an instance field
        :type raw_yaml:  str
        :type kwargs:    dict

        :raise: <???>
        """
        if raw_yaml and kwargs:
            raise #REALLY BAD (CAN'T PASS BOTH)
        if raw_yaml:
            try:
                self.args = yaml.loads(raw_yaml)
            except:
                raise # NOPE, not YAML actually
        else:
            self.args = kwargs
