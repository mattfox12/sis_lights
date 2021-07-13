#!/usr/bin/env python3
# White
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# White with a color temperature

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

def init(strip, table_values):
    global transition, time_start
    transition = 0
    time_start = 0
    # print "Init white pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start white timer {0}\n".format(time_start),
        # sys.stdout.flush()

    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),table_values["primary_color"],easeOut(transition)))
    else:
        fill(strip, table_values["primary_color"]) # fill with white

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
