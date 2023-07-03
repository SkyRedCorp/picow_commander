# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""PICOW COMMANDER - Automate and execute programs 
    without touching keyboard or mouse"""

# Import OS, Wi-Fi, and HTTPServer libraries
import os
import time
import board
import microcontroller
from digitalio import DigitalInOut, Direction

# Web Server and Socketpool libraries
import mdns
from adafruit_httpserver import Server, Request, GET, POST, FileResponse
import ipaddress
import wifi
import socketpool

#MDNS Server Config
mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "picow"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)

# Keystrokes library
import core.keystrokes as keystrokes

# Random number library
from random import randint

"""Creating objects for required libraries"""
#  Onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

# Connect to network
print()
print("Connecting to WiFi")

#  connect to your SSID
try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID2'), os.getenv('CIRCUITPY_WIFI_PASSWORD2'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static")

# Route default static
document_root = '/www'

@server.route("/")
def base(request: Request):
    return FileResponse(request, filename='index.html', root_path=document_root)

# Routing Server
@server.route("/", POST)
def buttonpress(request: Request):
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    
    # Browser select
    if "msedge" in raw_text:
        keystrokes.runas_app(os.getenv('msedge'))
        print("Starting MS Edge")

    elif "chrome" in raw_text:
        keystrokes.runas_app(os.getenv('chrome'))
        print("Starting Chrome")

    elif "firefox" in raw_text:
        keystrokes.runas_app(os.getenv('frefox'))
        print("Starting Firefox")

    elif "notepad" in raw_text:
        keystrokes.runas_app(os.getenv('txtpad'))
        print("Starting Notepad")

    # Windows commands
    elif "winlock" in raw_text:
        keystrokes.lock_win()
        print("Locking")
        
    elif "winunlock" in raw_text:
        keystrokes.unlock_win()
        print("unlocking")

    elif "winoff" in raw_text:
        keystrokes.runas_cmd(os.getenv('cmdoff'))
        print("Shutting Down")

    elif "winreboot" in raw_text:
        keystrokes.runas_cmd(os.getenv('reboot'))
        print("Rebooting")

    # Specific commands
    elif "onenote" in raw_text:
        keystrokes.runas_app(os.getenv('onenot'))
        print("Starting One Note")

    elif "outlook" in raw_text:
        keystrokes.runas_app(os.getenv('emailo'))
        print("Starting Outlook")

    elif "excel" in raw_text:
        keystrokes.runas_app(os.getenv('spread'))
        print("Starting Excel")

    elif "winword" in raw_text:
        keystrokes.runas_app(os.getenv('docsed'))
        print("Starting Word")
        
    # Task Manager
    elif "taskmgr" in raw_text:
        keystrokes.task_mgr()
        print("Starting Task manager")
        
    # Ctrl + Alt + Supr
    elif "ctalsu" in raw_text:
        keystrokes.panic_button()
        print("CTRL + ALT + SUPR")
    
    # Screen Shot
    elif "scrshot" in raw_text:
        keystrokes.scr_shot()
        print("Screen Shot!")

    else:
        print("Unknown command")
    
    return FileResponse(request, filename='index.html', root_path=document_root)

print("starting server..")
# Start of Server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Please access to: http://%s:80" % wifi.radio.ipv4_address)
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
