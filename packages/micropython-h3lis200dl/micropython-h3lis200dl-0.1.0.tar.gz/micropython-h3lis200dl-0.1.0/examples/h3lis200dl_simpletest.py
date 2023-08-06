# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_h3lis200dl import h3lis200dl

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
h3lis = h3lis200dl.H3LIS200DL(i2c)

while True:
    accx, accy, accz = h3lis.acceleration
    print("x:{:.2f}g, y:{:.2f}g, z{:.2f}g".format(accx, accy, accz))
    time.sleep(0.5)
