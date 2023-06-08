#!/usr/bin/env python3
# Name: Homing
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Alternating color bands, moving towards zero point

try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *

from timeit import default_timer as timer
# import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

current_primary = Color(255,255,255,24)
current_secondary = Color(0,0,255,0)

fullcount = 0
secondcount = 0
led_offset = 0
pixel_offset = 0

speed = 1.0     # theta multiplied
divisions = 3   # number of each color

old_offset = 0

def init(strip, table_values):
    global transition, time_start, fullcount, secondcount, led_offset, pixel_offset
    time_start = 0
    transition = 0
    # print "Init homing pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

    # figure out split
    fullcount = (strip.numPixels()+1) / divisions
    secondcount = fullcount / 2

    if table_values["led_offset"] != 0:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())
        # print("pixel_offset", pixel_offset, ", length ", strip.numPixels(), "\n"),
        # sys.stdout.flush()

    # print "count {0}, second {1}\n".format(fullcount, secondcount),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, speed, divisions, led_offset, pixel_offset, current_primary, current_secondary, fullcount, secondcount, old_offset

    if time_start == 0:
        time_start = timer()
        transition = 0

    half = int(strip.numPixels() / 2)
    offset = (transition % half) * 4

    if table_values["led_offset"] != 0 and led_offset != table_values["led_offset"]:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())
        # print("pixel_offset", pixel_offset, "length", strip.numPixels(), "half", half, "\n"),
        # sys.stdout.flush()

    if transition < 1.0:
        table_values["do_update"] = True
        for i in range(half+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            opp_index = (strip.numPixels() - i + pixel_offset) % strip.numPixels()

            index = ((i-1+offset) % strip.numPixels()) % fullcount
            if index < secondcount:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index), current_primary, easeOut(transition)))
                strip.setPixelColor(opp_index, colorBlend(strip.getPixelColor(opp_index), current_primary, easeOut(transition)))
            else:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index), current_secondary, easeOut(transition)))
                strip.setPixelColor(opp_index, colorBlend(strip.getPixelColor(opp_index), current_secondary, easeOut(transition)))
    elif old_offset != offset:
        table_values["do_update"] = True
        for i in range(half+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            opp_index = (strip.numPixels() - i + pixel_offset) % strip.numPixels()

            index = ((i-1+offset) % half) % fullcount
            if index < secondcount:
                if isDiff(current_primary, strip.getPixelColor(pixel_index)):
                    strip.setPixelColor(pixel_index, colorBlend(current_primary, strip.getPixelColor(pixel_index), 0.95))
                if isDiff(current_primary, strip.getPixelColor(opp_index)):
                    strip.setPixelColor(opp_index, colorBlend(current_primary, strip.getPixelColor(opp_index), 0.95))
            else:
                if isDiff(current_secondary, strip.getPixelColor(pixel_index)):
                    strip.setPixelColor(pixel_index, colorBlend(current_secondary, strip.getPixelColor(pixel_index), 0.95))
                if isDiff(current_secondary, strip.getPixelColor(opp_index)):
                    strip.setPixelColor(opp_index, colorBlend(current_secondary, strip.getPixelColor(opp_index), 0.95))

    old_offset = offset
    
    # increment time
    time_end = timer()
    transition += time_end - time_start
    time_start = time_end
