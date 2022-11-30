#!/usr/bin/env python3
# Name: Clock
# Author: Matthew Klundt (matt@withease.io)
#
# Description: Show hours, minutes, seconds via lights
# Uses: Primary, Secondary

from neopixel import *
import datetime
from timeit import default_timer as timer
import sys

from colorFunctions import fill
from colorFunctions import colorBlend
from easing import easeOut
from easing import easeInQuad

time_start = 0 # for elapsed time
transition = 0 # 0-1.0, fade between states

second_color = Color(0,0,0,0)

def init(strip, table_values):
    global transition, time_start, second_color
    time_start = 0
    transition = 0

    second_color = Color(255,255,255,255)
    # print "Init spread pattern {0} {1}\n".format(time_start, transition),
    # sys.stdout.flush()

def update(strip, table_values):
    global transition, time_start, second_color
    if time_start == 0:
        time_start = timer()
        transition = 0
        # print "Start spread timer {0}\n".format(time_start),
        # sys.stdout.flush()

    led_count = strip.numPixels()

    now = datetime.datetime.now()

    # print "Time {0}:{1}:{2}\n".format(now.hour, now.minute, now.second),

    hour_color = table_values["primary_color"]
    minute_color = table_values["secondary_color"]

    # color of background, set to the opposite of hour_color, so that it contrasts
    w1 = (hour_color >> 24) & 0xFF;
    r1 = (hour_color >> 16) & 0xFF;
    g1 = (hour_color >> 8) & 0xFF;
    b1 = hour_color & 0xFF;
    bg_color = Color((255-r1) >> 1,(255-g1) >> 1,(255-b1) >> 1,0)

    # Hour
    h_fixed = 360 - (now.hour * 30 + table_values["led_offset"]) % 360
    spread = 12
    spread_l = h_fixed - spread
    spread_r = h_fixed + spread

    h_start = int( (spread_l * led_count) / 360 )
    h_end = int( (spread_r * led_count) / 360 ) + 1
    if (h_end < h_start):
        h_end += led_count

    if transition < 1.0:
        for i in range(strip.numPixels()+1):
            if i < h_start%led_count or i > h_end%led_count:
                strip.setPixelColor(i, colorBlend(strip.getPixelColor(i),bg_color,easeOut(transition)))
    else:
        fill(strip, bg_color) # default color

    for x in range(h_start, h_end):
        pos = x % led_count
        strip.setPixelColor(pos, hour_color)

    # Minutes
    m_fixed = 360 - (now.minute * 6 + table_values["led_offset"]) % 360
    spread = 6
    spread_l = m_fixed - spread
    spread_r = m_fixed + spread

    m_start = int( (spread_l * led_count) / 360 )
    m_end = int( (spread_r * led_count) / 360 ) + 1
    if (m_end < m_start):
        m_end += led_count

    # print "Minute {0}, {1}:{2}\n".format(now.minute, m_start, m_end),

    for x in range(m_start, m_end):
        pos = x % led_count
        strip.setPixelColor(pos, minute_color)

    # Seconds
    s_fixed = 360 - (now.second * 6) % 360
    spread = 2
    spread_l = s_fixed - spread
    spread_r = s_fixed + spread

    s_start = int( (spread_l * led_count) / 360 )
    s_end = int( (spread_r * led_count) / 360 ) + 1
    if (s_end < s_start):
        s_end += led_count

    for x in range(s_start, s_end):
        pos = x % led_count
        strip.setPixelColor(pos, second_color)

    # draw
    strip.show()

    # increment time
    if transition < 1.0:
        time_end = timer()
        transition += time_end - time_start
        time_start = time_end
