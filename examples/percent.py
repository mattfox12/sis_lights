#!/usr/bin/env python3
# Name: Percent
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Fades between Primary (start) - Secondary (end), based on percent of track played
# Uses: Primary #ff330000, Secondary #0000ff00

# library changed names since our initial release, this imports the available one
try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import hsbBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

target_primary = Color(0,0,0,0)
target_secondary = Color(0,0,0,0)

old_percent = 0

def init(strip, table_values):
    global transition, time_start, percent
    time_start = 0
    transition = 0
    # print "Init percent pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, old_percent, target_primary, target_secondary
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start percent timer {0}\n".format(time_start),
        # sys.stdout.flush()
    
    percent = table_values["percent"]

    # if percent change is more than 5%, smooth to it 
    if abs(old_percent - percent) > 0.05:
        time_start = timer()
        transition = 0
        
	# reset target_color, transition if we are given a new primary_color
    if isDiff(table_values["primary_color"], target_primary):
        target_primary = table_values["primary_color"]
        time_start = timer()
        transition = 0
    if isDiff(table_values["secondary_color"], target_secondary):
        target_secondary = table_values["secondary_color"]
        time_start = timer()
        transition = 0

    if transition < 1.0:
        target_color = hsbBlend(target_primary,target_secondary,percent)
        for i in range(strip.numPixels()+1):
            strip.setPixelColor(i, hsbBlend(strip.getPixelColor(i),target_color,easeOut(transition)))
        table_values["do_update"] = True
    elif percent != old_percent:
        fill(strip, hsbBlend(target_primary,target_secondary,percent)) # fill with color based on rho only
        table_values["do_update"] = True

    old_percent = percent

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
