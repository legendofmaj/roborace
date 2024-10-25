#!/usr/bin/env python3

from time import sleep

from read_color_sensor import seesRed
import drop_packet

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.sensor import ColorSensor

#Define modules
btn = Button()
depositMotor = LargeMotor(OUTPUT_A) #Medium motor gave me an error
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

while True:
    #Check for button Input
    if btn.any():
        print("Button pressed!") #Debug only
        sleep(1)
        buttonPressed = True

    #Move the tank
    seconds = 3
    if buttonPressed == True:
        tankDrive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), seconds)

    #Check for colorRed
    colorDetected = ColorSensor.color()
    sleep(0.2)
    if colorDetected == 5:
        seesRed  = True
        print("seesRed") #Debug only
    else:
        seesRed = False
        print("doesn't seeRed") #Debug only



def Drop():
    #code to stop moving
    depositMotor.on_for_rotations(SpeedPercent(75), 2.25)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -2.25)
    time.sleep(0.5)
    #code to resume other programms