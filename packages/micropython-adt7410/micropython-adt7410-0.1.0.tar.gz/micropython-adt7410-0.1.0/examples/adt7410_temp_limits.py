# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adt7410 import adt7410

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adt = adt7410.ADT7410(i2c)

adt.low_temperature = 18
adt.high_temperature = 29
adt.critical_temperature = 35
adt.hysteresis_temperature = 2

print("High limit: {}C".format(adt.high_temperature))
print("Low limit: {}C".format(adt.low_temperature))
print("Critical limit: {}C".format(adt.critical_temperature))

adt.comparator_mode = adt7410.COMP_ENABLED

while True:
    print("Temperature: {:.2f}C".format(adt.temperature))
    alert_status = adt.alert_status
    if alert_status.high_alert:
        print("Temperature above high set limit!")
    if alert_status.low_alert:
        print("Temperature below low set limit!")
    if alert_status.critical_alert:
        print("Temperature above critical set limit!")
    time.sleep(1)
