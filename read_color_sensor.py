#!/usr/bin/env python3
# "slave"

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

def readColor():
    while True:
        sleep(0.2)
        colorDetected = ColorSensor.color
        #sleep(0.2)
        if colorDetected == 5:            
            seesRed  = True
            print("sees red")
            colorDetected = ColorSensor.color
        else:
            seesRed = False
            print("no red")
            colorDetected = ColorSensor.color


            #print("sees red")