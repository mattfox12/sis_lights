#!/usr/bin/env python3
# Name: Homing
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Alternating color bands, moving towards zero point

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

current_primary = Color(255,255,255,24)
current_secondary = Color(0,0,255,0)

fullcount = 0
secondcount = 0

speed = 1.0     # theta multiplied
divisions = 3   # number of each color

def init(strip, table_values):
    global transition, time_start, fullcount, secondcount
    time_start = 0
    transition = 0
    # print "Init homing pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

    # figure out split
    fullcount = (strip.numPixels()+1) / divisions
    secondcount = fullcount / 2

    # print "count {0}, second {1}\n".format(fullcount, secondcount),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, speed, divisions, current_primary, current_secondary, fullcount, secondcount

    if time_start == 0:
        time_start = timer()
        transition = 0

    half = strip.numPixels() / 2
    offset = (transition % half) * 4

    if transition < 1.0:
        for i in range(half+1):
            index = ((i-1+offset) % strip.numPixels()) % fullcount
            if index < secondcount:
                strip.setPixelColor(i, colorBlend(strip.getPixelColor(i), current_primary, easeOut(transition)))
                strip.setPixelColor(strip.numPixels()-i, colorBlend(strip.getPixelColor(strip.numPixels()-i), current_primary, easeOut(transition)))
            else:
                strip.setPixelColor(i, colorBlend(strip.getPixelColor(i), current_secondary, easeOut(transition)))
                strip.setPixelColor(strip.numPixels()-i, colorBlend(strip.getPixelColor(strip.numPixels()-i), current_secondary, easeOut(transition)))
    else:
        for i in range(half+1):
            index = ((i-1+offset) % half) % fullcount
            if index < secondcount:
                if isDiff(current_primary, strip.getPixelColor(i)):
                    strip.setPixelColor(i, colorBlend(current_primary, strip.getPixelColor(i), 0.95))
                if isDiff(current_primary, strip.getPixelColor(strip.numPixels()-i)):
                    strip.setPixelColor(strip.numPixels()-i, colorBlend(current_primary, strip.getPixelColor(strip.numPixels()-i), 0.95))
            else:
                if isDiff(current_secondary, strip.getPixelColor(i)):
                    strip.setPixelColor(i, colorBlend(current_secondary, strip.getPixelColor(i), 0.95))
                if isDiff(current_secondary, strip.getPixelColor(strip.numPixels()-i)):
                    strip.setPixelColor(strip.numPixels()-i, colorBlend(current_secondary, strip.getPixelColor(strip.numPixels()-i), 0.95))

    # increment time
    time_end = timer()
    transition += time_end - time_start
    time_start = time_end
