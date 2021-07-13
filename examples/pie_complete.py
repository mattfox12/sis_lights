#!/usr/bin/env python3
# Name: Pie Complete
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Lights up primary/secondary color based on percent of track played
# Uses: Primary, Secondary

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

led_offset = 0
pixel_offset = 0

def init(strip, table_values):
    global transition, time_start, led_offset, pixel_offset
    time_start = 0
    transition = 0
    # print "Init fade pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

    if table_values["led_offset"] != 0:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())
        # print "pixel_offset {0}, length {1}\n".format(pixel_offset, strip.numPixels()),
        # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, led_offset, pixel_offset
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start fade timer {0}\n".format(time_start),
        # sys.stdout.flush()

    if led_offset != table_values["led_offset"]:
        led_offset = table_values["led_offset"]
        pixel_offset = int((table_values["led_offset"] / 6.283) * strip.numPixels())

    percent = (1.0 - table_values["percent"]) * strip.numPixels()
    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            if i < percent:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index),table_values["primary_color"],easeOut(transition)))
            else:
                strip.setPixelColor(pixel_index, colorBlend(strip.getPixelColor(pixel_index),table_values["secondary_color"],easeOut(transition)))
    else:
        for i in range(strip.numPixels()+1):
            pixel_index = (i + pixel_offset) % strip.numPixels()
            if i < percent:
                strip.setPixelColor(pixel_index, table_values["primary_color"])
            else:
                strip.setPixelColor(pixel_index, table_values["secondary_color"])

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
