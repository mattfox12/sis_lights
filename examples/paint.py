#!/usr/bin/env python3
# Name: Paint
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: Paints a color based on position, leaving history of color

try:
    from neopixel import *
except ImportError:
    from rpi_ws281x import *

from timeit import default_timer as timer
from math import sin
import sys

from colorFunctions import hsbBlend
# from colorFunctions import colorBlend
from colorFunctions import wheel
from colorFunctions import isDiff
from easing import easeIn

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init spread pattern {0} {1}\n".format(time_start, transition),
    sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start

    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start spread timer {0}\n".format(time_start),
        sys.stdout.flush()

    # assign h_theta
    h_theta = table_values["theta"] * 57.2958

    h_fixed = h_theta % 360

    # if old_h != h_fixed:
    led_count = strip.numPixels()

    # print "Balls %s, Wheel %s\n" % (balls, int(rho*255 + theta*0.2) % 255),
    # sys.stdout.flush()

    # color of spread by ball
    # ball_color = wheel(int(rho*255)) # change based on rho
    ball_color = wheel(int(table_values["rho"]*255 + h_theta*0.2) % 255) # change based on rho (and theta)
    # ball_color = colorBlend(primary_color, secondary_color, rho) # blend between primary/secondary based on rho
    # ball_color = wheel(int(value*255)%255) # change based on rho + sine wave variation
    second_color = wheel(int(table_values["rho"]*255 + h_theta*0.2 - 128) % 255) # change based on rho (and theta)

    # spread out the pixel color based on rho
    spread = 15 # force to specific width
    spread_l = h_theta - spread
    spread_r = h_theta + spread

    start = int( (spread_l * led_count) / 360 )
    end = int( (spread_r * led_count) / 360 ) + 1
    if (end < start):
        end += led_count
    
    # print "Rho %s, Theta %s, Adjusted Theta %s\n" % (rho, theta, h_theta),
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
                strip.setPixelColor(pos, new_color)
                is_change = True

            # print "pos {0} ( {1} - {2} ) / {3}, percent {4}\n".format(pos, h_fixed, degrees, spread, t),
            # sys.stdout.flush()

    # second ball coloring
    if table_values["balls"] > 1:
        h_theta = h_theta + 180

        spread = 10 # force to specific width
        spread_l = h_theta - spread
        spread_r = h_theta + spread

        start = int( (spread_l * led_count) / 360 )
        end = int( (spread_r * led_count) / 360 ) + 1
        if (end < start):
            end += led_count

        h_fixed = h_theta % 360

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
                new_color = hsbBlend(second_color,strip.getPixelColor(pos),percent)
                if isDiff(strip.getPixelColor(pos), new_color):
                    strip.setPixelColor(pos, new_color)
                    is_change = True
        
    if is_change:
        table_values["do_update"] = True

    # increment time
    time_end = timer()
    if transition < 1.0:
        transition += time_end - time_start
    time_start = time_end
