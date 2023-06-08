#!/usr/bin/env python3
# Sisyphus Color Functions
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Commonly used color functions for RGBW lights

import time
# library changed names since our initial release, this imports the available one
try:
    from neopixel import Color
except ImportError:
    from rpi_ws281x import Color

def colorBlend(color1,color2,blend=0):
    """Returns a color at (blend) percent between color1 and color2."""
    if (blend > 1):
        blend = 1
    if (blend < 0):
        blend = 0
    w1 = (color1 >> 24) & 0xFF;
    r1 = (color1 >> 16) & 0xFF;
    g1 = (color1 >> 8) & 0xFF;
    b1 = color1 & 0xFF;
    w2 = (color2 >> 24) & 0xFF;
    r2 = (color2 >> 16) & 0xFF;
    g2 = (color2 >> 8) & 0xFF;
    b2 = color2 & 0xFF;
    red = int(r1+(r2-r1)*blend)
    green = int(g1+(g2-g1)*blend)
    blue = int(b1+(b2-b1)*blend)
    white = int(w1+(w2-w1)*blend)
    return Color(red,green,blue,white)

def hsbBlend(color1,color2,blend=0):
    """Returns a color at (blend) percent between color1 and color2 using Hue/Saturation/Black changes."""
    if (blend >= 1):
        return color2
    if (blend <= 0):
        return color1
    w1 = (color1 >> 24) & 0xFF;
    r1 = (color1 >> 16) & 0xFF;
    g1 = (color1 >> 8) & 0xFF;
    u1 = color1 & 0xFF; # blUe
    w2 = (color2 >> 24) & 0xFF;
    r2 = (color2 >> 16) & 0xFF;
    g2 = (color2 >> 8) & 0xFF;
    u2 = color2 & 0xFF; # blUe

    h1,s1,b1 = hsbFromRGB(r1,g1,u1)
    h2,s2,b2 = hsbFromRGB(r2,g2,u2)

    # blend hue based on shortest distance (5-355 in -10 steps instead of 350)
    tempH = h2-h1
    if (tempH > 180.0):
        tempH -= 360.0
    elif (tempH < -180.0):
        tempH += 360.0

    hue = h1+(tempH)*blend
    if (hue < 0.0):
        hue += 360.0
    elif (hue > 360.0):
        hue -= 360.0
    saturation = s1+(s2-s1)*blend
    black = b1+(b2-b1)*blend

    # print "HSB {0} {1} {2}\n".format(hue, saturation, black)

    red,green,blue = rgbFromHSB(hue,saturation,black)
    white = int(w1+(w2-w1)*blend) # blend as is

    # print "RGB {0} {1} {2}\n".format(red, green, blue)

    return Color(red,green,blue,white)

def hsbFromRGB(r,g,u):
    # convert RGB (0-255,0-255,0-255) to HSB (0-360.0,0-1.0,0-1.0)

    # define hsb vars
    h = 0.0
    s = 0.0
    b = 0.0

    # convert rgb 0-255 to float 0-1.0
    r = float(r)/255.0
    g = float(g)/255.0
    u = float(u)/255.0

    min1 = float(min(r, g, u))
    max1 = float(max(r, g, u))

    # black
    b = (max1 + min1) / 2

    if (min1 == max1):
        # grey
        h = 0
        s = 0
    else:
        # saturation
        if (b < 0.5):
            s = (max1-min1)/(max1+min1)
        elif (b >= 0.5):
            s = (max1-min1)/(2.0-max1-min1)

        # hue
        if (r == max1):
            h = (g-u)/(max1-min1)
        elif (g == max1):
            h = 2.0 + (u-r)/(max1-min1)
        elif (u == max1):
            h = 4.0 + (r-g)/(max1-min1)

        h *= 60.0
        if (h < 0.0):
            h += 360.0
        elif (h > 360.0):
            h = 0.0

    return h,s,b

def rgbFromHSB(h,s,b):
    # convert HSB (0-360.0,0-1.0,0-1.0) to RGB (0-255,0-255,0-255)

    # define rgb vars
    r = 0.0
    g = 0.0
    u = 0.0

    if (s == 0):
        r = b
        g = b
        u = b
    else:
        # define temp vars
        temp1 = 0.0
        temp2 = 0.0
        tempR3 = 0.0
        tempG3 = 0.0
        tempB3 = 0.0
        hueTemp = 0.0

        if (b < 0.5):
            temp2 = b * (1.0 + s)
        else:
            temp2 = (b + s) - (b * s)

        temp1 = (2.0 * b) - temp2

        hueTemp = h / 360.0

        # Red
        tempR3 = hueTemp + 1.0 / 3.0
        if (tempR3 < 0.0):
            tempR3 = tempR3 + 1.0
        elif (tempR3 > 1.0):
            tempR3 = tempR3 - 1.0

        # Green
        tempG3 = hueTemp
        if (tempG3 < 0.0):
            tempG3 = tempG3 + 1.0
        elif (tempG3 > 1.0):
            tempG3 = tempG3 - 1.0

        # Blue
        tempB3 = hueTemp - 1.0 / 3.0
        if (tempB3 < 0.0):
            tempB3 = tempB3 + 1.0
        elif (tempB3 > 1.0):
            tempB3 = tempB3 - 1.0

        # Red
        if (6.0 * tempR3 < 1.0):
            r = temp1 + (temp2 - temp1) * 6.0 * tempR3
        elif (2.0 * tempR3 < 1.0):
            r = temp2
        elif (3.0 * tempR3 < 2.0):
            r = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempR3) * 6.0
        else:
            r = temp1

        # Green
        if (6.0 * tempG3 < 1.0):
            g = temp1 + (temp2 - temp1) * 6.0 * tempG3
        elif (2.0 * tempG3 < 1.0):
            g = temp2
        elif (3.0 * tempG3 < 2.0):
            g = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempG3) * 6.0
        else:
            g = temp1

        # Blue
        if (6.0 * tempB3 < 1.0):
            u = temp1 + (temp2 - temp1) * 6.0 * tempB3
        elif (2.0 * tempB3 < 1.0):
            u = temp2
        elif (3.0 * tempB3 < 2.0):
            u = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempB3) * 6.0
        else:
            u = temp1

    return int(r*255.0),int(g*255.0),int(u*255.0)

def fill(strip, color):
    """Fill all pixels with one color."""
    for i in range(strip.numPixels()+1):
        strip.setPixelColor(i, color)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()+1):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def isSame(color1,color2):
    """Compares if two colors are the same."""
    w1 = (color1 >> 24) & 0xFF;
    r1 = (color1 >> 16) & 0xFF;
    g1 = (color1 >> 8) & 0xFF;
    b1 = color1 & 0xFF;
    w2 = (color2 >> 24) & 0xFF;
    r2 = (color2 >> 16) & 0xFF;
    g2 = (color2 >> 8) & 0xFF;
    b2 = color2 & 0xFF;

    if r1==r2 and g1==g2 and b1==b2 and w1==w2:
        return True
    else:
        return False

def isDiff(color1,color2):
    """Compares if two colors are the same."""
    return not isSame(color1,color2)

# return value from 0-1.0 (1.0 == identical)
def similarity(color1,color2):
    """Compares if two colors are the same."""
    w1 = (color1 >> 24) & 0xFF;
    w2 = (color2 >> 24) & 0xFF;
    wS = 1.0 - (abs(w2-w1)/255.0)

    r1 = (color1 >> 16) & 0xFF;
    r2 = (color2 >> 16) & 0xFF;
    rS = 1.0 - (abs(r2-r1)/255.0)

    g1 = (color1 >> 8) & 0xFF;
    g2 = (color2 >> 8) & 0xFF;
    gS = 1.0 - (abs(g2-g1)/255.0)

    b1 = color1 & 0xFF;
    b2 = color2 & 0xFF;
    bS = 1.0 - (abs(b2-b1)/255.0)

    return (wS + rS + gS + bS)/4.0