#!/usr/bin/env python3
# Name: Mono Paint
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Paints a monochromatic color based on position, leaving history of color
# Uses: Primary

# library changed names since our initial release, this imports the available one
try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *
from timeit import default_timer as timer
from math import sin 
# import sys

from colorFunctions import hsbBlend
from colorFunctions import hsbFromRGB
from colorFunctions import rgbFromHSB
from colorFunctions import isDiff
from easing import easeIn

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

old_h = 0

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init paint pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, old_h

    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start paint timer {0}\n".format(time_start),
        # sys.stdout.flush()

    # assign h_theta
    h_theta = table_values["theta"] * 57.2958

    h_fixed = h_theta % 360

    led_count = strip.numPixels()

    # print "Balls %s, Wheel %s\n" % (balls, int(table_values["rho"]*255 + table_values["theta"]*0.2) % 255),
    # sys.stdout.flush()

    # values for controlling sine wave
    rho_reduction = 51 # used for scaling Rho to angle, higher number makes hue change faster with Rho change
    angle_reduction = 0.2 # the larger the number, the faster it changes (affects Rho + Theta)
    hue_range =  25 # in degrees, how far color will change in hue from Primary Color

    # color of spread by ball
    ball_color = table_values["primary_color"] 
    w1 = (ball_color >> 24) & 0xFF;
    r1 = (ball_color >> 16) & 0xFF;
    g1 = (ball_color >> 8) & 0xFF;
    u1 = ball_color & 0xFF;
    h1,s1,b1 = hsbFromRGB(r1,g1,u1)
    # sine wave x degrees around Hue of selected color, based on rho/theta, reduced
    angle = (table_values["rho"]*rho_reduction + h_theta*0.2) * angle_reduction
    h2 = h1 + sin(angle) * hue_range
    # recreate color from new HSB
    r2,g2,u2 = rgbFromHSB(h2,s1,b1)
    ball_color = Color(r2,g2,u2,w1)

    # spread out the pixel color based on theta
    spread = 15 # force to specific width
    spread_l = h_theta - spread
    spread_r = h_theta + spread

    start = int( (spread_l * led_count) / 360 )
    end = int( (spread_r * led_count) / 360 ) + 1
    if (end < start):
        end += led_count

    # print "Rho %s, Theta %s, Adjusted Theta %s\n" % (table_values["rho"], table_values["theta"], h_theta),
    # sys.stdout.flush()
    is_change = False

    for x in range(start, end):
        pos = x % led_count
        degrees = (float(pos * 360) / led_count)

        # fix wrapping degrees
        if (degrees > h_fixed + 180):
            degrees -= 360
        elif (degrees < h_fixed - 180):
            degrees += 360

        # ramp brightness
        t = abs(h_fixed - degrees) / spread

        if t > 0 and t <= 1.0:
            percent = easeIn(t) # choose an ease function from above
            new_color = hsbBlend(ball_color,strip.getPixelColor(pos),percent)
            if isDiff(strip.getPixelColor(pos), new_color):
                is_change = True
                strip.setPixelColor(pos, new_color)

            # print "pos {0} ( {1} - {2} ) / {3}, percent {4}\n".format(pos, h_fixed, degrees, spread, t),
            # sys.stdout.flush()
            
    # Update if it changed (i.e.: if you pause, it might not anymore)
    if is_change:
        table_values["do_update"] = True

    # increment time
    time_end = timer()
    if transition < 1.0:
        transition += time_end - time_start
    time_start = time_end
