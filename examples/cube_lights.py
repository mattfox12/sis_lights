#!/usr/bin/env python3
# Name: Cube Lights
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Lights matching the position of X and Y 
# Uses: Primary #00f2ff84, Secondary #00035e00

try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *

# from math import pow
from timeit import default_timer as timer
import sys
from math import sqrt

from sisyphusType import SisyphusType

from colorFunctions import fill
from colorFunctions import isSame
from colorFunctions import colorBlend
from easing import easeInQuad as easeIn
from easing import easeOut

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

radius = 1

old_h = 0

def init(strip, table_values):
    global transition, time_start, radius
    time_start = 0
    transition = 0
    
    # we know the ratio and light count, we can figure out side length
    led_count = strip.numPixels()
    height = table_values["y_length"]
    width = led_count / 2 - height
    
    if table_values["type"] == SisyphusType.XYLA:
        radius = sqrt(width*width + height*height) / 2
    
    print("Init Cube Lights pattern", width, height, radius)
    sys.stdout.flush()

def draw_pixel(strip, ball_color, i, offset, dir):
    blend = offset - int(offset)
    if blend > 0.25 and blend < 0.75:
        blend = (blend - 0.25) * 2 # scale up blend from 0.25-0.75 to scale of 0-1.0
        strip.setPixelColor(int(i + offset * dir), colorBlend(strip.getPixelColor(int(i + offset * dir)),ball_color,easeIn(1.0-blend)))
        strip.setPixelColor(int(i + (offset + 1) * dir), colorBlend(strip.getPixelColor(int(i + (offset + 1) * dir)),ball_color,easeIn(blend)))
    else:
        if blend >= 0.75 and blend < 1.0:
            strip.setPixelColor(int(i + (offset + 1) * dir), ball_color)
        else:
            strip.setPixelColor(int(i + offset * dir), ball_color)

def update(strip, table_values):
    global transition, time_start, old_h, radius
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start calibrate timer {0}\n".format(time_start),
        sys.stdout.flush()

    led_count = strip.numPixels()
    
    # colors
    ball_color = table_values["primary_color"]
    bg_color = table_values["secondary_color"]

    fill(strip, bg_color) # default color
    
    if table_values["type"] == SisyphusType.XYLA:
        
        # we know the ratio and light count, we can figure out side length
        height = table_values["y_length"]
        width = led_count / 2.0 - height
        margin = 1 # pixels on edges to skip
        
        # color pixel at x/y value (both sides)
        x0 = ((table_values["x"]+table_values["width"]/2) / table_values["width"]) * (width - margin * 2) + margin
        y0 = ((table_values["y"]+table_values["height"]/2) / table_values["height"]) * (height - margin * 2) + margin
        
        # print("W/H ", width, ", ", height, "\n")
        # print("X/Y ", table_values["x"], ", ", table_values["y"], "\n")
        # print("Start ", x0, ", ", y0, "\n")
        # sys.stdout.flush()

        # set X axis lights to line up with ball
        draw_pixel(strip, ball_color, height, x0, 1)
        draw_pixel(strip, ball_color, height + width + height + width, x0, -1)

        # set Y axis lights to line up with ball
        draw_pixel(strip, ball_color, 0, y0, 1)
        draw_pixel(strip, ball_color, height + width + height, y0, -1)

        # lights at 1/2 points of x axis
        x1 = x0 / 2
        draw_pixel(strip, ball_color, height, x1, 1)
        draw_pixel(strip, ball_color, height + width + height + width, x1, -1)
        x2 = (width - x0) / 2 + x0
        draw_pixel(strip, ball_color, height, x2, 1)
        draw_pixel(strip, ball_color, height + width + height + width, x2, -1)

        # lights at 1/2 points of y axis
        y1 = y0 / 2
        draw_pixel(strip, ball_color, 0, y1, 1)
        draw_pixel(strip, ball_color, height + width + height, y1, -1)
        y2 = (height - y0) / 2 + y0
        draw_pixel(strip, ball_color, 0, y2, 1)
        draw_pixel(strip, ball_color, height + width + height, y2, -1)
        
        table_values["do_update"] = True
    
    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
