# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel
import digitalio

pixel_pin = board.GP0
num_pixels = 8

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

out = digitalio.DigitalInOut(board.GP15)
out.direction = digitalio.Direction.OUTPUT
out.value = True

""" led = digitalio.DigitalInOut(board.LED) """

def setOn(pin):
    out = digitalio.DigitalInOut(pin)
    out.direction = digitalio.Direction.OUTPUT
    out.value = False

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for k in range(2):
        for j in range(255):
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(rc_index & 255)
            pixels.show()
            time.sleep(wait)

def soft_on(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixels[i] = (j, j, j)
        pixels.show()
        time.sleep(wait)


def soft_off(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixels[i] = (255-j, 255-j, 255-j)
        pixels.show()
        time.sleep(wait)
        
def toggle(pin: DigitalInOut):
    if pin.value:
        pin.value = False
    else:
        pin.value = True
    

if (1 == 0):
    for pin in [board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP23, board.GP24, board.GP25]:
        setOn(pin)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
WHITE_L = (180, 180, 180)
BLACK = (0, 0, 0)

print("Turning off")
pixels.fill(BLACK)
pixels.show()
time.sleep(1)
print("Start demo")


while True:
    toggle(out)
    soft_on(0.002)
    time.sleep(1)
    soft_off(0.002)
    time.sleep(1)
    
    rainbow_cycle(0.01)  # Increase the number to slow down the rainbow
    
    pixels.fill(RED)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLACK)
    pixels.show()
    time.sleep(1)

    pixels.fill(WHITE_L)
    pixels.show()
    time.sleep(5)

    pixels.fill(WHITE)
    pixels.show()
    time.sleep(5)


    pixels.fill(RED)
    pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)

    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow
