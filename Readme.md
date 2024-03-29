# Sisyphus Lights Primer

Making light patterns for your RGBW Sisyphus can be done by writing a Python script. Uploading is allowed starting with Sisbot version 1.10.88. Starting with Sisbot 1.12.17, an additional table_state "do_update" value was added. This value needs to be set to True in order for the lights to update their color values. Ideally, you optimize your pattern to not send data if no light colors have changed.

## Auto-fill parameters

At the top of the Python script, include the following comments to have the Sisyphus auto-fill the name, description, and color values.

* Name: name of the pattern
* Author: your name
* Description: text users will see, describing the pattern
* Uses: select the color options shown for this pattern, and optional default color White, Primary (#0000ff00), and Secondary (#ff000000)

White is singular, if it is shown, Primary and Secondary are not. Secondary is not shown unless Primary is also shown. Starting in Sisbot version 1.12.22, you can also include the default color values to set when uploaded to Sisyphus.

## Expected Functions

There are two expected (but optional) functions that will be used to run a light pattern script, init(strip, table_state) and update(strip, table_state). Init is useful to set up initial values when your script is loaded (e.g. time of day, index numbers, etc). Update brings new data into your running script, as well as the reference to the current LED strip.

### Table_state

Table_state dictionary contains all exposed values of the current state of the Sisyphus. Values include:

* theta (in radians)
* rho (0-1.0)
* type (POLAR or XYLA)
* x (XYLA only, x position, 0 is center)
* y (XYLA only, y position, 0 is center)
* width (XYLA only, width of sandfield)
* height (XYLA only, height of sandfield)
* y_length (XYLA only, pixel length of y-axis)
* ratio (XYLA only, ratio of W/H)
* state (playing/homing,etc)
* balls (1-2)
* primary_color
* secondary_color
* percent (amount of current track completed: 0-1.0)
* led_offset (offset for zero point, in radians)
* do_update (True|False)

Theta automatically accounts for led_offset, but if your pattern depends on knowing where the zero point is, led_offset is there to calculate it. Currently, only Sisyphus Mini (LE/EX/ES) have an led_offset that is not zero. The value of led_offset can be changed by the user in Settings->Advanced Settings->Advanced Lights via the slider.

## Neopixel library

The LED strip is controlled using Adafruit NeoPixel library, documentation on it can be found at [circuitpython.readthedocs.io/projects/neopixel](https://circuitpython.readthedocs.io/projects/neopixel/en/latest/)

## Helper Functions

Included in the src folder are sisyphusState.py, sisyphusType.py, colorFunctions.py, and easing.py. These files contain a number of functions that you can use to simplify the code to change colors, smooth between values, and more. On the Sisyphus, these files reside in the same folder as the pattern Python files.

### SisyphusState

This file contains an Enumerator class for knowing the current Sisyphus state. Please compare using the enumerator as values may change in the future. Current values include WAITING, PLAYING, PAUSED, HOMING, and SLEEPING. Access/compare using variables such as: SisyphusState.WAITING

### SisyphusType

Starting in Sisbot version 1.12.22, this file contains an Enumerator class for knowing the current Sisyphus model. Please compare using the enumerator as values may change in the future. Current values include POLAR, XYLA. Access/compare using variables such as: SisyphusType.XYLA

### ColorFunctions
* colorBlend(color1,color2,blend=0): Returns a color at (blend) percent between color1 and color2 on RGB channels.
* hsbBlend(color1,color2,blend=0): Returns a color at (blend) percent between color1 and color2 via blending Hue/Saturation/Black.
* fill(strip, color): Fill all pixels with one color.
* colorWipe(strip, color, wait_ms=50): Wipe color across strip a pixel at a time. Wipe will finish before any other code executes.
* wheel(pos): Returns rainbow color within 0-255 pos(itions).
* isSame(color1,color2): Compare if two colors are identical
* isDiff(color1,color2): Compare if two colors are different
* similarity(color1,color2): Gives a float value of how similar the two colors are to each other. 0.0 == completely different, 1.0 == identical

## Simple example

	#!/usr/bin/env python3
	# Name: Solid
	# Author: Your Name
	# Description: Solid color
	# Uses: Primary #ff000000
	try:
		from neopixel import *
	except ImportError:
		from rpi_ws281x import *
	from colorFunctions import fill
	def init(strip, table_state):
		fill(strip, table_values["primary_color"]) # fill with primary
		table_values["do_update"] = True # required since 1.12.17 to tell lights to refresh

## Uploading to Sisyphus

Navigate via a web browser to Settings->Advanced Settings->Advanced Lights. Click the "+Add Pattern" button, and select your Python file.
