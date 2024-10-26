#!/usr/bin/env python3
# "master"

from time import sleep

import read_color_sensor
#import drop_packet

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button

#Define modules
btn = Button()
m = LargeMotor(OUTPUT_B)

while True:
    sleep(1)
    #if btn.any():
        #print("Button pressed!")
        #m.on_for_rotations(SpeedPercent(-75), 5)     
        #sleep(1)
    #if seesRed == True:
        #drop_packet.Drop()
        #print("happy")
    #elif seesRed == False:
        #print("blind")
    read_color_sensor.readColor()
