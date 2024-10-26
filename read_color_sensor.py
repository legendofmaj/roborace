#!/usr/bin/env python3
# "slave"

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

while True:
    colorDetected = ColorSensor.color
    sleep(0.2)
    if colorDetected == 5:
        print("sees red")
        seesRed  = True
    else:
        seesRed = False