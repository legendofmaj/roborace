#!/usr/bin/env python3

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

colorSensor = ColorSensor(INPUT_1)

def main():
    print("on")
    while True:
        readColor()
        sleep(2)

def readColor():
    global seesRed
    #global seesRed #Why is the global keyword necessary here? The variable was defined outside of a function. Is it used somewhere else?
    colorDetected = colorSensor.color
    col_raw = [0, 0, 0]
    col_raw = colorSensor.raw
    print(colorSensor.raw) #debug
    if (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]: # method of guestemating if smth is green, seems to work better than the integrated function, can be adjusted for all rgb base colors
        print("thinks green")
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
    print(colorSensor.color_name)

main()