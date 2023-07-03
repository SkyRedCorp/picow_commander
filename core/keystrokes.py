# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""Library used for Execute commands in Windows OS"""

# Import OS, Wi-Fi, and HTTPServer libraries
import os
import time
import board

# USB HID Libraries
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse

# Random number library
from random import randint

# AES encryption Module
import core.skrcrypt as skrcrypt

name = "keystrokes"

"""Creating objects for required libraries"""
# HID
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# List of Adafruit Keyboard strokes (You can Add as much as you need)
key_pad = [Keycode.GUI, Keycode.UP_ARROW, Keycode.ENTER,
           Keycode.DELETE, Keycode.DOWN_ARROW, Keycode.RIGHT_SHIFT,
           Keycode.LEFT_SHIFT, Keycode.ALT, Keycode.BACKSPACE,
           Keycode.TAB, Keycode.RIGHT_ARROW, Keycode.LEFT_ARROW,
           Keycode.PRINT_SCREEN, Keycode.SPACE, Keycode.CAPS_LOCK,
           Keycode.ESCAPE, Keycode.CONTROL]

key_ltr = [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E,
           Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J,
           Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O,
           Keycode.P, Keycode.Q, Keycode.R, Keycode.S, Keycode.T,
           Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y,
           Keycode.Z]

key_num = [Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR,
           Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT,
           Keycode.NINE, Keycode.ZERO]

key_dot = [Keycode.PERIOD, Keycode.COMMA, Keycode.QUOTE,
           Keycode.EQUALS]

key_fun = [Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5,
           Keycode.F6, Keycode.F7, Keycode.F8, Keycode.F9, Keycode.F10,
           Keycode.F11, Keycode.F12]

# Definition of Keyboard functions
""" WINDOWS KEY + LETTER """
def windows_ltr(keystr2):
    keyboard.send(key_pad[0], key_ltr[keystr2])
    time.sleep(0.5)
    
""" DECRYPT STRING """
def decrypt_str():
    keystring = os.getenv('keystr')
    hexstring = os.getenv('cryptk')
    decrypted = skrcrypt.decrypt_string(keystring, hexstring)
    return decrypted

""" START APP THROUGH RUN PROGRAM """
def runas_app(command_str):
    windows_ltr(17)
    time.sleep(0.5)
    cmd_str = layout.write(command_str)
    keyboard.send(key_pad[2])
    
""" START APP THROUGH CMD PROMPT """
def runas_cmd(command_pad):
    windows_ltr(17)
    time.sleep(0.5)
    layout.write(os.getenv('cshell'))
    keyboard.send(key_pad[2])
    time.sleep(1)
    cmd_str = layout.write(command_pad)
    keyboard.send(key_pad[2])
    
""" LOCK: WINDOWS KEY + L """
def lock_win():
    windows_ltr(11)
    
""" UNLOCK: ENTER + PASSWORD + ENTER """
def unlock_win():
    keyboard.send(key_pad[2])
    time.sleep(1)
    layout.write(decrypt_str())
    keyboard.send(key_pad[2])
    
""" START TASK MANAGER """
def task_mgr():
    keyboard.send(key_pad[16], key_pad[5], key_pad[15])
    time.sleep(0.5)

""" ADVANCED SCREENSHOT """
def scr_shot():
    keyboard.send(key_pad[0], key_pad[5], key_ltr[18])
    time.sleep(0.5)
    
""" CTRL + ALT + SUPR """
def panic_button():
    keyboard.send(key_pad[16], key_pad[7], key_pad[3])
    time.sleep(0.5)
    
# Definition of Mouse functions
def mice_jiggle():
    WAIT_TIME = 10
    for each in range(randint(1, 4)):
        x = randint(1, 50)
        y = randint(1, 50)
        mouse.move(x, y)
        mouse.move(-x, -y)
    time.sleep(WAIT_TIME)
