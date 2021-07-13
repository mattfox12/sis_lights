#!/usr/bin/env python3
# Name: Rainbow
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Rainbow gradient, follows ball position

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import colorBlend
from colorFunctions import wheel
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init rainbow pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start rainbow timer {0}\n".format(time_start),
        # sys.stdout.flush()

    led_count = strip.numPixels()

    # offset of rainbow
    wheel_deg = int(((-table_values["theta"] * 57.2958) % 360) / 360 * 255)
    # print "theta %s = %s \n" % (theta, wheel_deg),

    for i in range(0,led_count):
        pixel_offset = float(i)/led_count*255.0
        offset = (int(pixel_offset)+wheel_deg) & 255;
        # print "%d wheel_deg %s degrees + pixel_offset %s = %s \n" % (i, wheel_deg, pixel_offset, offset),
        if transition < 1.0:
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i), wheel(offset),easeOut(transition)))
        else:
            strip.setPixelColor(i, wheel(offset))

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
