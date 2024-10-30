#!/usr/bin/env python3

import time
import threading 
import sys

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

btn = Button()
tankDrive = MoveTank(OUTPUT_A, OUTPUT_B)
colorSensor = ColorSensor(INPUT_1)

def main():
    while True:
        buttonFun()
        if buttonPressed == True:
            break #This should work, because only when the first fun reaches break, will the second loop be reached
    while True:
        colorFun()
        tankFun()
        if colorFun() == "red":
            break
    
    #ToDo: Step 3: Rotate around until distance to next house is ca. 80cm
    

def buttonFun():
    global buttonPressed
    buttonPressed = False
    if btn.any() == True:
        buttonPressed = True
    time.sleep(0.1)

def tankFun():
    tankDrive.on_for_seconds(SpeedPercent(-50), SpeedPercent(-50), 15)

def colorFun():
    global color
    color = "none"
    rawColor = colorSensor.color
    if rawColor == 5:
        color = "red"
    elif rawColor == 3:
        color = "green"
    return color


if __name__=="__main__":
    main()