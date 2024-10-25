#!/usr/bin/env python3

from time import sleep

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.sensor import ColorSensor

#Define modules
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

#Button functions
def buttonPressed():
    #Check for button Input
    while True:
        if btn.any():
            print("Button pressed!") #Debug only
            sleep(1)
            buttonPressed = True
            return buttonPressed
def moveTank():
    #Move the tank
    seconds = 3
    if buttonPressed == True:
        tankDrive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), seconds)

def checkForColor():
    #Check for colorRed
    colorWanted = 5
    colorDetected = ColorSensor.color()
    sleep(0.2)
    if colorDetected == colorWanted:
        seesRed  = True
        print("seesRed") #Debug only
    else:
        seesRed = False
        print("doesn't seeRed") #Debug only

def Drop():
    #code to stop moving
    depositMotor.on_for_rotations(SpeedPercent(75), 2.25)
    sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -2.25)
    sleep(0.5)
    #code to resume other programms