# Sisyphus Lights Primer

Making light patterns for your RGBW Sisyphus can be done by writing a Python script. Uploading is allowed starting with Sisbot version 1.10.88.

## Expected Functions

There are two expected (but optional) functions that will be used to run a light pattern script, init(strip, table_state) and update(strip, table_state). Init is useful to set up initial values when your script is loaded (e.g. time of day, index numbers, etc). Update brings new data into your running script, as well as the reference to the current LED strip.

### Table_state

Table_state dictionary contains all exposed values of the current state of the Sisyphus. Values include:

* theta (in radians)
* rho (0-1.0)
* state (playing/homing,etc)
* balls (1-2)
* primary_color
* secondary_color
* percent (amount of current track completed: 0-1.0)
* led_offset (offset for zero point, in radians)

Theta automatically accounts for led_offset, but if your pattern depends on knowing where the zero point is, led_offset is there to calculate it. Currently, only Sisyphus Mini (LE/EX/ES) have an led_offset that is not zero. The value of led_offset can be changed by the user in Settings->Advanced Settings->Advanced Lights via the slider.

## Neopixel library

The LED strip is controlled using Adafruit NeoPixel library, documentation on it can be found at [circuitpython.readthedocs.io/projects/neopixel](https://circuitpython.readthedocs.io/projects/neopixel/en/latest/)

## Helper Functions

Included in the src folder are sisyphusState.py, colorFunctions.py, and easing.py. These files contain a number of functions that you can use to simplify the code to change colors, smooth between values, and more. On the Sisyphus, these files reside in the same folder as the pattern Python files.

### SisyphusState

This file contains an Enumerator class for knowing the current Sisyphus state. Please compare using the enumerator as values may change in the future. Current values include WAITING, PLAYING, PAUSED, HOMING, and SLEEPING. Access/compare using variables such as: SisyphusState.WAITING

### ColorFunctions
* colorBlend(color1,color2,blend=0): Returns a color at (blend) percent between color1 and color2 on RGB channels.
* hsbBlend(color1,color2,blend=0): Returns a color at (blend) percent between color1 and color2 via blending Hue/Saturation/Black.
* fill(strip, color): Fill all pixels with one color.
* colorWipe(strip, color, wait_ms=50): Wipe color across strip a pixel at a time. Wipe will finish before any other code executes.
* wheel(pos): Returns rainbow color within 0-255 pos(itions).
* isSame(color1,color2): Compare if two colors are identical
* isDiff(color1,color2): Compare if two colors are different

## Simple example

	from neopixel import *
	from colorFunctions import fill
	def init(strip, table_state):
		fill(strip, Color(255,0,0,0)) # fill with red

## Uploading to Sisyphus

Navigate via a web browser to Settings->Advanced Settings->Advanced Lights. Click the "+Add Pattern" button, and select your Python file.
