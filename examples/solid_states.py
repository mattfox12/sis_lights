#!/usr/bin/env python3
# Name: Solid States
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Description: All lights primary color, change based on table state
# Uses: Primary

from neopixel import *
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from colorFunctions import isDiff
from easing import easeOut

from sisyphusState import SisyphusState

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

current_color = Color(0,0,0,0)
target_color = Color(0,0,0,0)

waiting_color = Color(0,255,0,0) # Green
paused_color = Color(255,0,0,0) # Red
homing_color = Color(0,0,255,0) # Blue
sleeping_color = Color(0,0,0,255) # White

def init(strip, table_values):
    global transition, time_start
    time_start = 0
    transition = 0
    # print "Init solid pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, current_color, target_color, waiting_color, paused_color, homing_color, sleeping_color
    if time_start == 0:
        time_start = timer()
        transition = 0
        target_color = table_values["primary_color"]
        # print "Start solid timer {0}\n".format(time_start),
        # sys.stdout.flush()

    # change color based on state
    if table_values["state"] == SisyphusState.WAITING:
        current_color = waiting_color
    elif table_values["state"] == SisyphusState.PAUSED:
        current_color = paused_color
    elif table_values["state"] == SisyphusState.HOMING:
        current_color = homing_color
    elif table_values["state"] == SisyphusState.SLEEPING:
        current_color = sleeping_color
    else:
        current_color = table_values["primary_color"]

    # reset target_color, transition if we are given a new primary_color
    if isDiff(current_color, target_color):
        target_color = current_color
        transition = 0
        time_start = timer() # reset

    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),target_color,easeOut(transition)))
    else:
        fill(strip, target_color) # fill with color

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
