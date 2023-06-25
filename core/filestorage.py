# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""Created for handle microSD card module"""

# Import OS, Core and SD libraries
import os
import adafruit_sdcard
import board
import busio
import digitalio
import storage

# Check File
from core.checkfile import file_exists

name = "filestorage"

# Chip Select Port
SD_CS = digitalio.DigitalInOut(board.GP13)

# SPI protocol ports
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO) # For Adafruit RP2040 Boards
spi = busio.SPI(board.GP10, board.GP11, board.GP12) # For Raspberry Pi Pico and Pico W 

# Used for Adafruit SD Card library
sdcard = adafruit_sdcard.SDCard(spi, SD_CS)

# Storage type and mount
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

#strfile = []

# Hex String file function (List of strings to put in Run command)
def hexstringfile(strfile):
    arrfile = []
    if(file_exists("/sd/hexstring2.txt")):
        with open("/sd/hexstring2.txt", "r") as f:
            lines = f.readlines()
            print("Reading HexString file...")
            for line in lines:
                arrfile.append(line)
        return arrfile

# KeyPad file function (List of Key Strokes - Experimental)
def keypadfile(keyfile):
    arrfile = []
    if(file_exists("/sd/keypad.txt")):
        with open("/sd/keypad.txt", "r") as f:
            lines = f.readlines()
            print("Reading KeyPad file...")
            for line in lines:
                arrfile.append(line)
        return arrfile

# Command list File function (List of Commands to response)
def cmdfile(cmdlistfile):
    arrfile = []
    
    if(file_exists("/sd/keypad.txt")):
        with open("/sd/keypad.txt", "r") as f:
            lines = f.readlines()
            print("Reading KeyPad file...")
            for line in lines:
                arrfile.append(line)
        return arrfile
    
    with open("/sd/cmdfile.txt", "r") as f:
        lines = f.readlines()
        print("Reading CMDFile...")
        for line in lines:
            arrfile.append(line.strip())
    return arrfile