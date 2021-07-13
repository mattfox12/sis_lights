#!/usr/bin/env python3
# Sisyphus State Values
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Use these states to know current state of Sisyphus

class SuperEnum(object):
    class __metaclass__(type):
        def __iter__(self):
            for item in self.__dict__:
                if item == self.__dict__[item]:
                    yield item

class SisyphusState(SuperEnum):
	WAITING = 0
	PLAYING = 1
 	PAUSED = 2
	HOMING = 3
	SLEEPING = 4
