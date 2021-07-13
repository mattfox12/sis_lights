#!/usr/bin/env python3
# Name: Fan
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Alternating color bands, move at faster than theta speed
# Uses: Primary, Secondary

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

from sisyphusState import SisyphusState

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

current_primary = Color(0,0,0,0)
current_secondary = Color(0,0,0,0)

fullcount = 0
secondcount = 0

speed = 3.0     # theta multiplied
divisions = 3   # number of each color

def init(strip, table_values):
    global transition, time_start, fullcount, secondcount
    time_start = 0
    transition = 0
    # print "Init fan pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

    # figure out split
    fullcount = strip.numPixels() / divisions
    secondcount = fullcount / 2

    # print "count {0}, second {1}\n".format(fullcount, secondcount),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, speed, divisions, current_primary, current_secondary, fullcount, secondcount

    if time_start == 0:
        time_start = timer()
        transition = 0
        current_primary = table_values["primary_color"]
        current_secondary = table_values["secondary_color"]
        # print "Start solid timer {0}\n".format(time_start),
        # sys.stdout.flush()

    # reset target_color, transition if we are given a new primary_color
    if isDiff(current_primary, table_values["primary_color"]) or isDiff(current_secondary, table_values["secondary_color"]):
        current_primary = table_values["primary_color"]
        current_secondary = table_values["secondary_color"]
        transition = 0
        time_start = timer() # reset

    offset = int(((-table_values["theta"]*speed) % 6.283) / 6.283 * strip.numPixels())

    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            index = ((i-1+offset) % strip.numPixels()) % fullcount
            if index < secondcount:
                strip.setPixelColor(i, colorBlend(strip.getPixelColor(i), current_primary, easeOut(transition)))
            else:
                strip.setPixelColor(i, colorBlend(strip.getPixelColor(i), current_secondary, easeOut(transition)))
    else:
        for i in range(strip.numPixels()+1):
            index = ((i-1+offset) % strip.numPixels()) % fullcount
            if index < secondcount:
                if isDiff(current_primary, strip.getPixelColor(i)):
                    strip.setPixelColor(i, colorBlend(current_primary, strip.getPixelColor(i), 0.5))
            else:
                if isDiff(current_secondary, strip.getPixelColor(i)):
                    strip.setPixelColor(i, colorBlend(current_secondary, strip.getPixelColor(i), 0.5))

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
