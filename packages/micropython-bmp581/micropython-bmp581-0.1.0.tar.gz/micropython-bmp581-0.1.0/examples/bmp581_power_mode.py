# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_bmp581 import bmp581

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
bmp = bmp581.BMP581(i2c)

bmp.power_mode = bmp581.NORMAL

while True:
    for power_mode in bmp581.power_mode_values:
        print("Current Power mode setting: ", bmp.power_mode)
        for _ in range(10):
            press = bmp.pressure
            print("pressure:{:.2f}kPa".format(press))
            time.sleep(0.5)
        bmp.power_mode = power_mode
