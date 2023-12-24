#!/usr/bin/env python3
# Sisyphus Type Values
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Use these types to know current kind of Sisyphus

class SuperEnum(object):
    class __metaclass__(type):
        def __iter__(self):
            for item in self.__dict__:
                if item == self.__dict__[item]:
                    yield item

class SisyphusType(SuperEnum):
    POLAR = 0
    XYLA = 1
