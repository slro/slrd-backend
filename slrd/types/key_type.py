# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
""" """


class KeyType(object):
    """ """

    def __init__(self, yaml_str=None, **kwargs):
        """ """

        if yaml_str:
            self.__init__(**yaml.loads(yaml_str))


