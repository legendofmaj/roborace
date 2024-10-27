#!/usr/bin/env python3

import time
import sys
import threading
import colorSensorTest

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank

#Define modules
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
consoleInput = "undefined"


def main():
    print("Enter moveTank to test basic tank steering")
    print("Enter drop to test the drop motor")
    threading1 = threading.Thread(target=readInputAndAct)
    threading1.start()
    while True:      
        time.sleep(0.5)
        if consoleInput != "undefined":
            moveTank()
            drop()
        colorSensorTest.main()
        if colorSensorTest.seesRed == True:
            drop()
            #code muss am ende so sein dass der rober es nicht dauerhaft wiederholt
            

def moveTank():
    #Move the tank
    seconds = 3
    global consoleInput
    if consoleInput == "moveTank":
        print("moving") #debug
        tankDrive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), seconds)
        consoleInput = "undefined"


def drop():
    global consoleInput
    if consoleInput == "drop":
        consoleInput = "undefined"
        print("dropping") #debug
        depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
        time.sleep(0.5)
        depositMotor.on_for_rotations(SpeedPercent(75), -1.9)
        time.sleep(0.5)


def readInputAndAct():
    while True:
        time.sleep(1)
        print("seeking") #debug
        userInput = input()
        print("input:" + userInput) #debug
        global consoleInput
        consoleInput = userInput 



main()