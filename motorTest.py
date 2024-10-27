#!/usr/bin/env python3

import time
import sys
import threading

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank

#Define modules
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)



def main():
    consoleInput = "undefined"
    print("Enter moveTank to test basic tank steering")
    print("Enter drop to test the drop motor")
    threading1 = threading.Thread(target=readInputAndAct, args=("consoleInput", consoleInput))
    threading1.start()
    while True:      
        time.sleep(1)
        threading1.join()
        if consoleInput != "undefined":
            moveTank(consoleInput)
            drop(consoleInput)
        else:
            print("undefined")
            

def moveTank(consoleInput):
    #Move the tank
    seconds = 3
    inputArg = consoleInput
    if inputArg == "moveTank":
        print("moving")
        tankDrive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), seconds)

def drop(consoleInput):
    inputArg = consoleInput
    if inputArg == "drop":
        print("dropping")
        depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
        time.sleep(0.5)
        depositMotor.on_for_rotations(SpeedPercent(75), -1.9)
        time.sleep(0.5)

def readInputAndAct(filler, consoleInput):
    while True:
        time.sleep(1)
        #filler = filler
        print("seeking")
        consoleInput = input()
        print("input:" + consoleInput)
        return consoleInput




main()