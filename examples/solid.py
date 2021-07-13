#!/usr/bin/env python3
# Name: Solid
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: All lights primary color
# Uses: Primary

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

target_color = Color(0,0,0,0)

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init solid pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, target_color
    if time_start == 0:
        time_start = timer()
        transition = 0
        target_color = table_values["primary_color"]
        # print "Start solid timer {0}\n".format(time_start),
        # sys.stdout.flush()

    # reset target_color, transition if we are given a new primary_color
    if isDiff(table_values["primary_color"], target_color):
        target_color = table_values["primary_color"]
        transition = 0
        time_start = timer() # reset

    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_color,easeOut(transition)))
    else:
        fill(strip, table_values["primary_color"]) # fill with color

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
