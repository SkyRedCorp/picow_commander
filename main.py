# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""PICOW COMMANDER - Automate and execute programs 
    without touching keyboard or mouse"""

# Import OS, Wi-Fi, and HTTPServer libraries
import os
import time
import ipaddress
import wifi
import socketpool
import board
import microcontroller
from digitalio import DigitalInOut, Direction
from adafruit_httpserver import Server, Request, Response, POST

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

# SD card readfile
import core.filestorage as filestorage

"""Creating objects for required libraries"""
# HID
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

#  Onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

# Array for reading hexstring.txt file
strfile = []
key_str = filestorage.hexstringfile(strfile)

# List of Adafruit Keyboard strokes (You can Add as much as you need)
key_pad = [Keycode.GUI, Keycode.R, Keycode.M, Keycode.UP_ARROW,
           Keycode.ENTER, Keycode.DELETE, Keycode.DOWN_ARROW,
           Keycode.L]

print("HexString File loaded successfully")

# Connect to network
print()
print("Connecting to WiFi")

#  Set static IP address
ipv4 =  ipaddress.IPv4Address("10.0.20.160")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("10.0.20.254")

# Set alternate IP Address
#ipv4 =  ipaddress.IPv4Address("192.168.1.100")
#netmask =  ipaddress.IPv4Address("255.255.255.0")
#gateway =  ipaddress.IPv4Address("192.168.1.254")

wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
#wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID2'), os.getenv('CIRCUITPY_WIFI_PASSWORD2'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

#  font for HTML
font_family = "monospace"

#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html{{font-family: {font_family}; background-color: lightblue;
        display:inline-block; margin: 0px auto; text-align: center;}}
        h1{{color: blue; width: 200; word-wrap: break-word; padding: 2vh; font-size: 28px;}}
        p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
        .button{{font-family: {font_family};display: inline-block;
        background-color: black; border: none;
        border-radius: 4px; color: white; padding: 10px 10px;
        text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer; width: 35%;}}
        p.dotted {{margin: auto;
        width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>SkyRed Web Commander</title>
    <h1>Pico W HTTP Server</h1>
    <br>
    <p class="dotted">Made to save time (And energy) :P</p>
    <br>
    <h1>Press the button according to the command you need</h1><br>
    <table>
        <tr>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN1" value="msedge" type="submit">MSEdge</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN2" value="chrome" type="submit">Chrome</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN3" value="firefox" type="submit">Firefox</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN4" value="notepad" type="submit">Notepad</button></a>
            </form>
        </tr>
        <p></p>
        <tr>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN5" value="winlock" type="submit">Lock</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN6" value="winunlock" type="submit">Unlock</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN7" value="winoff" type="submit">Shutdown</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN8" value="winreboot" type="submit">Reboot</button></a>
            </form>
        </tr>
        <p></p>
        <tr>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN9" value="onenote" type="submit">OneNote</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN10" value="outlook" type="submit">Outlook</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN11" value="excel" type="submit">Excel</button></a>
            </form>
            <form accept-charset="utf-8" method="POST">
            <button class="button" name="BTN12" value="winword" type="submit">Word</button></a>
            </form>
        </tr>
    </table>
    </body></html>
    """
    return html

# Definition of functions
def run_shortcut(keystr2):
    keyboard.send(key_pad[0], key_pad[keystr2])
    time.sleep(0.5)

def decrypt_str():
    keystring = key_str[9].strip()
    hexstring = key_str[4].strip()
    decrypted = skrcrypt.decrypt_string(keystring, hexstring)
    return decrypted

def runas_app(command_str):
    run_shortcut(1)
    time.sleep(0.5)
    cmd_str = layout.write(command_str)
    
def runas_cmd(command_pad):
    run_shortcut(1)
    time.sleep(0.5)
    layout.write(key_str[2])
    time.sleep(0.5)
    cmd_str = layout.write(command_pad)
    
def run_lock(keystr1):
    keyboard.send(key_pad[0], key_pad[keystr1])

def run_shortcut(keystr2):
    keyboard.send(key_pad[0], key_pad[keystr2])

def unlockdevice():
    keyboard.send(key_pad[4])
    time.sleep(1)
    layout.write(decrypt_str())
    keyboard.send(key_pad[4])

# Route default static IP
@server.route("/")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html')

# Routing Server
@server.route("/", POST)
def buttonpress(request: Request):
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    # Browser select
    if "msedge" in raw_text:
        runas_app(key_str[8])
        print("Starting MS Edge")

    elif "chrome" in raw_text:
        runas_app(key_str[11])
        print("Starting Chrome")

    elif "firefox" in raw_text:
        runas_app(key_str[12])
        print("Starting Firefox")

    elif "notepad" in raw_text:
        runas_app(key_str[1])
        print("Starting Notepad")

    # Windows commands
    elif "winlock" in raw_text:
        run_lock(7)
        print("Locking")
        
    elif "winunlock" in raw_text:
        unlockdevice()
        print("unlocking")

    elif "winoff" in raw_text:
        runas_cmd(key_str[5])
        print("Shutting Down")

    elif "winreboot" in raw_text:
        runas_cmd(key_str[3])
        print("Rebooting")

    # Specific commands
    elif "onenote" in raw_text:
        runas_app(key_str[7])
        print("Starting One Note")

    elif "outlook" in raw_text:
        runas_app(key_str[6])
        print("Starting Outlook")

    elif "excel" in raw_text:
        runas_app(key_str[13])
        print("Starting Excel")

    elif "winword" in raw_text:
        runas_app(key_str[14])
        print("Starting Word")
        
    else:
        print("Unknown command")
    
    return Response(request, f"{webpage()}", content_type='text/html')

print("starting server..")
# Start of Server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
# In case the server fails, reboots the Pico W
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()
ping_address = ipaddress.ip_address("8.8.4.4")

clock = time.monotonic()

while True:
    try:
        # Every 30 secs make a Ping, to certify it's connected
        if (clock + 30) < time.monotonic():
            if wifi.radio.ping(ping_address) is None:
                print("lost connection")
            else:
                print("connected")
            clock = time.monotonic()
        else:
            server.poll()
    except Exception as e:
        print(e)
        continue