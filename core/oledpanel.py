# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""SSD1306 OLED Library
   Used for show Options and IP address"""

#OS libraries
import time
import board
import busio

#Helper libraries
import displayio
import terminalio
from adafruit_display_text import label

#OLED Libraries
import adafruit_displayio_ssd1306

name = "oledpanel"

#Release any display, clearing I2C ports
displayio.release_displays()

#I2C Settings
i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 32
BORDER = 2

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

def ipadd(iptext):
	text = iptext
	text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=HEIGHT // 2 - 1)
	splash.append(text_area)
	display.refresh()
