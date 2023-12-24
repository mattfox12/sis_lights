#!/usr/bin/env python3
# Name: Checkers
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: XYLA checkered colors on width and height sides
# Uses: Primary #00ff0000, Secondary #0000ff00

try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *

from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

did_show = False
old_x = 0
old_y = 0
target_primary = Color(0,0,0,0)
target_secondary = Color(0,0,0,0)

def init(strip, table_values):
    global transition, time_start, did_show
    time_start = 0
    transition = 0
    did_show = False
    # print "Init box pattern {0} {1}\n".format(time_start, transition),
    sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, target_primary, target_secondary, old_x, old_y, did_show
    if time_start == 0:
        time_start = timer()
        transition = 0
        target_primary = table_values["primary_color"]
        target_secondary = table_values["secondary_color"]
        # print "Start box timer {0}\n".format(time_start),
        # sys.stdout.flush()

    # reset target_primary, transition if we are given a new primary_color
    if isDiff(table_values["primary_color"], target_primary):
        target_primary = table_values["primary_color"]
        transition = 0
        time_start = timer() # reset
        did_show = False
    if isDiff(table_values["secondary_color"], target_secondary):
        target_secondary = table_values["secondary_color"]
        transition = 0
        time_start = timer() # reset
        did_show = False
    
    # we know the ratio and light count, we can figure out side length
    height = table_values["y_length"]
    width = strip.numPixels() / 2.0 - height
    margin = 1
    
    x1 = ((table_values["x"]+table_values["width"]/2) / table_values["width"]) * (width - margin * 2) + margin
    y1 = ((table_values["y"]+table_values["height"]/2) / table_values["height"]) * (height - margin * 2) + margin
    
    if x1 != old_x or y1 != old_y:
        did_show = False

    if transition < 1.0:
        fill(strip, target_primary) # default color
        
        for i in range(0, int(y1)):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_secondary,easeOut(transition)))
        for i in range(int(height), int(height+x1)):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_secondary,easeOut(transition)))
        for i in range(int(height+width), int(height+width+height-y1)):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_secondary,easeOut(transition)))
        for i in range(int(height+width+height), int(height+width+height+width-x1)):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_secondary,easeOut(transition)))
            
        table_values["do_update"] = True
    elif did_show == False:
        fill(strip, target_primary) # default color
        
        for i in range(0, int(y1)):
            strip.setPixelColor(i, target_secondary)
        for i in range(int(height), int(height+x1)):
            strip.setPixelColor(i, target_secondary)
        for i in range(int(height+width), int(height+width+height-y1)):
            strip.setPixelColor(i, target_secondary)
        for i in range(int(height+width+height), int(height+width+height+width-x1)):
            strip.setPixelColor(i, target_secondary)
            
		# blend on pos
        blend_x = x1 - int(x1)
        blend_y = y1 - int(y1)
        strip.setPixelColor(int(y1), colorBlend(target_primary,target_secondary,easeOut(blend_y)))
        strip.setPixelColor(int(height+x1), colorBlend(target_primary,target_secondary,easeOut(blend_x)))
        strip.setPixelColor(int(height+width+height-y1), colorBlend(target_primary,target_secondary,easeOut(1.0-blend_y)))
        strip.setPixelColor(int(height+width+height+width-x1), colorBlend(target_primary,target_secondary,easeOut(1.0-blend_x)))
            
        did_show = True
        table_values["do_update"] = True
        
    old_x = x1
    old_y = y1

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
