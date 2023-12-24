#!/usr/bin/env python3
# Sisyphus Ease Functions
# Author: Matthew Klundt (matt@sisyphus-industries.com)
#
# Commonly used easing functions for RGBW lights

def clamp(t):
    if t > 1.0:
        return 1.0
    elif t < 0:
        return 0
    else:
        return t

def easeIn(t):
    t = clamp(t)
    return 1.0 - pow(2, (1.0 - t) * 10.0) / 1024.0

def easeOut(t):
    t = clamp(t)
    return pow(2, t * 10.0) / 1024.0

def easeInQuad(t):
    t = clamp(t)
    return t*t

def easeOutQuad(t):
    t = clamp(t)
    return 1-(1-t)*(1-t)

def easeInCubic(t):
    t = clamp(t)
    return t*t*t

def easeOutCubic(t):
    t = clamp(t)
    return 1-pow(1-t,3)

def easeInQuart(t):
    t = clamp(t)
    return t*t*t*t

def easeOutQuart(t):
    t = clamp(t)
    return 1 - pow( 1 - t, 4 )

def easeInOutExpo(t):
    t = clamp(t)
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2