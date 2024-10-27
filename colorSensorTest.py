#!/usr/bin/env python3

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

colorSensor = ColorSensor(INPUT_1)

def main():
    while True:
        readColor()
        sleep(1)

def readColor():
    colorDetected = colorSensor.color
    if colorDetected == 5:
        seesRed = True
        print(seesRed)
    else:
        seesRed = False
        #print(seesRed)

#main()    