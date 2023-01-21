# SPDX-FileCopyrightText: Minborg
#
# SPDX-License-Identifier: Apache 2

import time
import board
import digitalio

pin = board.GP1
out = digitalio.DigitalInOut(pin)
out.direction = digitalio.Direction.OUTPUT
out.value = True
print(pin)


def toggle():
    if out.value:
        out.value = False
    else:
        out.value = True
        

while True:
    toggle()
    time.sleep(0.125)
