# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import ipaddress
import wifi
import socketpool
#import busio
import board
import microcontroller
from digitalio import DigitalInOut, Direction
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
import neopixel

print("Starting up...")

# Any language
COLS = 11
ROWS = 10

# SE

panel = [
    "klockantärk",
    "femyistioni",
    "kvartqienzo",
    "tjugolivipm",
    "överkamhalv",
    "ettusvlxtvå",
    "tremykyfyra",
    "femsflorsex",
    "sjuåttainio",
    "tioelvatolv"
]

it_is_leds = list(range(7))+list(range(8,10))

fem     = {1: range(3)}
fem_i   = {1: list(range(3))+list([4])}
tio     = {1: range(6, 9)}
tio_i   = {1: list(range(6, 9))+list([9])}
kvart   = {2: range(5)}
kvart_i = {2: list(range(5))+list([6])}
över    = {4: range(4)}
tjugo   = {3: range(5)}
tjugo_i = {3: list(range(5))+list([6])}
halv    = {4: range(7, 11)}

words = {
    0: [],
    1: [fem, över],
    2: [tio, över],
    3: [kvart, över],
    4: [tjugo, över],
    5: [fem_i, halv],
    6: [halv],
    7: [fem, över, halv],
    8: [tjugo_i],
    9: [kvart_i],
   10: [tio_i],
   11: [fem_i],
}

digits = {
    1: {5: range(3)},
    2: {5: range(8,11)},
    3: {6: range(3)},
    4: {6: range(7, 11)},
    5: {7: range(3)},
    6: {7: range(8, 11)},
    7: {8: range(3)},
    8: {8: range(3, 7)},
    9: {8: range(8, 11)},
   10: {9: range(3)},
   11: {9: range(3, 7)},
   12: {9: range(7, 11)},
}

#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

#  pin used for party parrot animation
parrot_pin = DigitalInOut(board.GP1)
parrot_pin.direction = Direction.OUTPUT
parrot_pin.value = False

print(time.localtime())

# Neopixel

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = YELLOW

pixel_pin = board.GP0
num_pixels = ROWS * COLS
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

#  connect to network
print()
print("Connecting to WiFi...")

#  set static IP address
ipv4 =  ipaddress.IPv4Address("192.168.1.42")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.1")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
#  connect to your SSID
print(os.getenv('CIRCUITPY_WIFI_SSID'))
print("Logging in...")
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

led.value = True
print("Connected to WiFi " + os.getenv('CIRCUITPY_WIFI_SSID'))
pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

#  variables for HTML
#  comment/uncomment desired temp unit

#  temp_test = str(ds18.temperature)
#  unit = "C"
temp_test = str(microcontroller.cpu.temperature)
frequency_mhz = str(microcontroller.cpu.frequency/1_000_000)
unit = "C"
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
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <br>
    <p class="dotted">This is a Pico W running an HTTP server with CircuitPython.</p>
    <br>
    <br>
    <p class="dotted">{renderPanel()}</p>
    <br>
    <br>
    <p class="dotted">The current CPU temperature for the Pico W is
    <span style="color: deeppink;">{temp_test}°{unit} and the frequency is {frequency_mhz} MHz</span></p><br>
    <h1>Control the LED on the Pico W with these buttons:</h1><br>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="LED ON" value="ON" type="submit">LED ON</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED OFF" value="OFF" type="submit">LED OFF</button></a></p></form>
    <h1>Party?</h>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="party" value="party" type="submit">PARTY!</button></a></p></form>
    </body></html>
    """
    return html


def wordClock():
    hour_dict = {1: "one",2: "two",3: "three",4: "four",5: "five",6: "six",7: "seven",8: "eight",9: "nine",10: "ten",11: "eleven",12: "twelve"}
    
    h = time.localtime().tm_hour
    h_12 = h % 12
    m = time.localtime().tm_min
    mm = m if m < 30 else 60 - m
    
    five    = mm in range(5,9) or mm in range(25, 29)
    ten     = mm in range(10, 14)
    quarter = mm in range(15,19)
    twenty  = mm in range(20, 29)
    o_clock = m in range(0, 4)

    over = m in range(4, 29)
    to   = m in range(31, 59)
    
    dots = m % 5
    
    r = f"""{h}:{m} -> it is """
    if (twenty):
        r += " twenty"
    if (five):
        r += " five"
    if (ten):
        r += " ten"
    if (quarter):
        r += " quarter"
    if (over):
        r += " over"
    if (to):
        r += " to"
    r = r + " " + hour_dict[h_12]
    if (o_clock):
        r += " o'clock"
        
    r += " ["
    for i in range(0, dots):
        r += "+"
    r += "]"

    return r    

def renderPanel():
    global panel, words, ROWS, COLS
      
    h = time.localtime().tm_hour
    m = time.localtime().tm_min
    
    arr = wordArray()
   
    result = ""
    for row in range(ROWS):
        for col in range(COLS):
            result += arr[row][col]
        result += "<br/>"

    return result


def wordArray():
    global panel, words
      
    h = time.localtime().tm_hour
    m = time.localtime().tm_min
    
    arr = [["." for col in range(11)] for row in range(10)]

    for col in it_is_leds:
        arr[0][col] = panel[0][col]
        
    m_div5 = int(m / 5);
    
    word = words[m_div5];   
    for mappings in word:
        for row in mappings:
            for col in mappings[row]:
                arr[row][col] = panel[row][col]
    
    digit = digits[h % 12]
    for row in digit:
        for col in digit[row]:
            arr[row][col] = panel[row][col]

    return arr


#  route default static IP
@server.route("/")
def base(request: HTTPRequest):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

#  if a button is pressed on the site
@server.route("/", method=HTTPMethod.POST)
def buttonpress(request: HTTPRequest):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    #  if the led on button was pressed
    if "ON" in raw_text:
        #  turn on the onboard LED
        # led.value = True
        parrot_pin.value = False # Pull down
    #  if the led off button was pressed
    if "OFF" in raw_text:
        #  turn the onboard LED off
        # led.value = False
        parrot_pin.value = True
    #  if the party button was pressed
    if "party" in raw_text:
        #  toggle the parrot_pin value
        parrot_pin.value = not parrot_pin.value
    #  reload site
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

def led(row, col):
    global COLS
    return row * COLS + col

def bootLeds():
    global ROWS
    global COLS
    global pixels
    global BLACK
    for row in range(ROWS):
        for max_col in range(COLS+4):
            pixels.fill(BLACK)
            for col in range(max(0, max_col-4), min(COLS, max_col)):
                pixels[led(row, col)] = COLOR
                
            pixels.show()
            time.sleep(0.03)
    pixels.fill(BLACK)
    pixels.show()

def renderLeds(old_array, array):
    global pixels
    global BLACK
    new_pixels = list()
    old_pixels = list()

    #for col in range(COLS):
    #    for row in range(ROWS):
    #        if array[row][col] != '.' and old_array[row, col] == '.':
    #            new_pixels = new_pixels + led(row, col)
    #        if array[row][col] == '.' and old_array[row, col] != '.':
    #            old_pixels = old_pixels + led(row, col)

    print("old pixels:", old_pixels)
    print("new pixels:", new_pixels)

    pixels.fill(BLACK)
    for col in range(COLS):
        for row in range(ROWS):
            if array[row][col] != '.':
                pixels[led(row, col)] = COLOR
    pixels.show()
    return

print("starting server..")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()
ping_address = ipaddress.ip_address("8.8.4.4")


print("Booting Neopixels...")
bootLeds()
print("Neopixels live")

clock = time.monotonic() #  time.monotonic() holder for server ping

pixel_clock = 0 # check the clock pixels. Trigger this at first loop
array = wordArray()
old_array = [["." for col in range(COLS)] for row in range(ROWS)]

while True:
    try:
        #  every 30 seconds, ping server 
        if (clock + 30) < time.monotonic():
            print("Ping")
            clock = time.monotonic()
            if wifi.radio.ping(ping_address) is None:
                print("lost connection")
                led.value = False
            else:
                print("connected")
                led.value = True

        
        # every second, check clock
        if (pixel_clock + 1 < time.monotonic()):
            pixel_clock = time.monotonic()
            # Toggle each second
            parrot_pin.value = not parrot_pin.value
            
            array = wordArray()
            if (array != old_array):
                renderLeds(old_array, array)
                old_array = array

        #  poll the server for incoming/outgoing requests
        server.poll()
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        continue

