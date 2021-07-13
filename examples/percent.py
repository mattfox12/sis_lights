#!/usr/bin/env python3
# Name: Percent
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Fade between primary/secondary color based on percent of track played
# Uses: Primary, Secondary

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import hsbBlend
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init fade pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start fade timer {0}\n".format(time_start),
        # sys.stdout.flush()

    percent = table_values["percent"]
    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            strip.setPixelColor(i, hsbBlend(strip.getPixelColor(i),hsbBlend(table_values["primary_color"],table_values["secondary_color"],percent),easeOut(transition)))
    else:
        fill(strip, hsbBlend(table_values["primary_color"],table_values["secondary_color"],percent)) # fill with color based on rho only

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
