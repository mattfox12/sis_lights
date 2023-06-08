#!/usr/bin/env python3
# Name: Line Complete
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Wipe from Primary (start) to Secondary (end) color, based on percent of track played
# Uses: Primary, Secondary

# library changed names since our initial release, this imports the available one
try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *
from timeit import default_timer as timer
import sys

# from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

led_offset = 0
pixel_offset = 0

target_primary = Color(0,0,0,0)
target_secondary = Color(0,0,0,0)

did_show = False
old_percent = 0

def init(strip, table_values):
    global transition, time_start, led_offset, pixel_offset, did_show
    time_start = 0
    transition = 0
    # print "Init fade pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

    if table_values["led_offset"] != 0:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())
        did_show = False
        # print "pixel_offset {0}, length {1}\n".format(pixel_offset, strip.numPixels()),
        # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, led_offset, pixel_offset, old_percent, did_show, target_primary, target_secondary

    if time_start == 0:
        time_start = timer()
        transition = 0
        target_primary = table_values["primary_color"]
        target_secondary = table_values["primary_color"]
        # print "Start fade timer {0}\n".format(time_start),
        # sys.stdout.flush()

    if led_offset != table_values["led_offset"]:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())
        did_show = False

    # reset target_color, transition if we are given a new primary_color
    if isDiff(table_values["primary_color"], target_primary):
        target_primary = table_values["primary_color"]
        transition = 0
        time_start = timer() # reset
        did_show = False

    # reset target_color, transition if we are given a new secondary
    if isDiff(table_values["secondary_color"], target_secondary):
        target_secondary = table_values["secondary_color"]
        transition = 0
        time_start = timer() # reset
        did_show = False

    percent = (1.0 - table_values["percent"]) * strip.numPixels()
    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            if i < percent:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index),target_primary,easeOut(transition)))
            else:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index),target_secondary,easeOut(transition)))
        table_values["do_update"] = True
    elif percent != old_percent or did_show == False:
        for i in range(strip.numPixels()+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            if i < percent:
                strip.setPixelColor(pixel_index, target_primary)
            else:
                strip.setPixelColor(pixel_index, target_secondary)
        did_show = True
        table_values["do_update"] = True

    old_percent = percent

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
