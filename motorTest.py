#!/usr/bin/env python3

from time import sleep

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank

#Define modules
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def main():
    consoleInput = "undefined"
    print("Enter moveTank to test basic tank steering")
    print("Enter drop to test the drop motor")
    while True:
        consoleInput = input()
        if consoleInput != "undefined":     
            sleep(1)
            moveTank(consoleInput)
            drop(consoleInput)


def moveTank(consoleInput):
    #Move the tank
    seconds = 3
    inputArg = consoleInput
    if inputArg == "moveTank":
        tankDrive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), seconds)

def drop(consoleInput):
    inputArg = consoleInput
    if inputArg == "drop":
        depositMotor.on_for_rotations(SpeedPercent(75), 2.25)
        sleep(0.5)
        depositMotor.on_for_rotations(SpeedPercent(75), -2.25)
        sleep(0.5)

main()