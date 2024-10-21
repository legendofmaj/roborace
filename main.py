#!/usr/bin/env python3

from time import sleep

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button

#Define modules
btn = Button()
m = LargeMotor(OUTPUT_A)

while True:
    if btn.any():
        print("Button pressed!")
        m.on_for_rotations(SpeedPercent(75), 5)     
        sleep(1)
