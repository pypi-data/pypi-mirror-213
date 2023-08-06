# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_isl29125 import isl29125

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
isl = isl29125.ISL29125(i2c)

while True:
    red, green, blue = isl.colors
    print("Red Luminance: ", red)
    print("Green Luminance: ", green)
    print("Blue Luminance:", blue)
    time.sleep(1)
