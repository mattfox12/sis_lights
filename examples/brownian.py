#!/usr/bin/env python3
# Name: Brownian
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Move away randomly from Primary Color
# Uses: Primary #ff000000

# library changed names since our initial release, this imports the available one
try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *
from timeit import default_timer as timer
import sys
from random import random

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

target_color = Color(0,0,0,0)

friction = 0.9
vel_range = 0.025
vel_list = list(())

def init(strip, table_values):
    global transition, time_start, vel_list
    time_start = 0
    transition = 0

    for i in range(strip.numPixels()+1):
        vel_list.append(0.0) # red velocity
        vel_list.append(0.0) # red value
        vel_list.append(0.0) # green velocity
        vel_list.append(0.0) # green value
        vel_list.append(0.0) # blue velocity
        vel_list.append(0.0) # blue value
        vel_list.append(0.0) # white velocity
        vel_list.append(0.0) # white value

    print "Init brownian pattern: {0}, {1}\n".format(strip.numPixels(), len(vel_list)),
    sys.stdout.flush()

def clamp(num):
    if num > 255.0:
        return 255.0
    elif num < 0.0:
        return 0.0
    else:
        return num

def update(strip, table_values):
    global transition, time_start, target_color, vel_list, friction
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
    elif transition < 1.5:
        fill(strip, target_color) # fill with color

        for i in range(strip.numPixels()+1):
            color1 = strip.getPixelColor(i)
            w1 = (color1 >> 24) & 0xFF;
            r1 = (color1 >> 16) & 0xFF;
            g1 = (color1 >> 8) & 0xFF;
            b1 = color1 & 0xFF;

            index = (i-1) * 8
            vel_list[index+1] = float(r1) # value
            vel_list[index+3] = float(g1) # value
            vel_list[index+5] = float(b1) # value
            vel_list[index+7] = float(w1) # value
    else:
        for i in range(strip.numPixels()+1):
            color1 = strip.getPixelColor(i)
            w1 = (color1 >> 24) & 0xFF;
            r1 = (color1 >> 16) & 0xFF;
            g1 = (color1 >> 8) & 0xFF;
            b1 = color1 & 0xFF;

            index = (i-1)*8
            vel_list[index] += random() * vel_range - vel_range/2.0     # velocity
            vel_list[index+2] += random() * vel_range - vel_range/2.0   # velocity
            vel_list[index+4] += random() * vel_range - vel_range/2.0   # velocity
            vel_list[index+6] += random() * vel_range - vel_range/2.0   # velocity

            vel_list[index+1] = clamp(vel_list[index]+vel_list[index+1]) # value
            vel_list[index+3] = clamp(vel_list[index+2]+vel_list[index+3]) # value
            vel_list[index+5] = clamp(vel_list[index+4]+vel_list[index+5]) # value
            vel_list[index+7] = clamp(vel_list[index+6]+vel_list[index+7]) # value

            vel_list[index] *= friction     # velocity
            vel_list[index+2] *= friction   # velocity
            vel_list[index+4] *= friction   # velocity
            vel_list[index+6] *= friction   # velocity

            new_color = Color(int(vel_list[index+1]), int(vel_list[index+3]), int(vel_list[index+5]), int(vel_list[index+7]))

            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),new_color,0.5))

	# always update
    table_values["do_update"] = True

    # increment time
    if transition < 1.5:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
