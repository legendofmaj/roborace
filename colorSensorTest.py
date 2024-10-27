#!/usr/bin/env python3

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

colorSensor = ColorSensor(INPUT_1)

def main():
    while True:
        readColor()

def readColor():
    colorDetected = colorSensor.color
    print(colorSensor.raw) #debug
    if colorDetected == 5:
        seesRed = True
        seesGreen = False
        print("sees Red: " + str(seesRed)) #debug
    elif colorDetected == 3:
        seesRed = False
        seesGreen = True
        print("seesGreen: " + str(seesGreen)) #debug
    else:
        seesRed = False
        seesGreen = False   