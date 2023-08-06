# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_isl29125 import isl29125

switch_pin = Pin(5, Pin.IN)

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
isl = isl29125.ISL29125(i2c)

print("Current High Threshold: ", isl.high_threshold)
print("Current Low Threshold: ", isl.low_threshold)
isl.interrupt_threshold = isl29125.BLUE_INTERRUPT
print("Setting up Blue Threshold window to 100-300 Lux")
isl.high_threshold = 300
isl.low_threshold = 100
print("Current High Threshold: ", isl.high_threshold)
print("Current Low Threshold: ", isl.low_threshold)

while True:
    print("INT Pin Value:", switch_pin.value)
    isl.clear_register_flag()
    red, green, blue = isl.colors
    print("Red Luminance: ", red)
    print("Green Luminance: ", green)
    print("Blue Luminance:", blue)

    time.sleep(1.5)
