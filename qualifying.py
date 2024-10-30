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
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)

def main():
    print("start")
    buttonThread = threading.Thread(target= buttonFun)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target= colorFun)
    colorThread.start()
    print("threads on")
    while True:
        if buttonPressed == True:
            print("button pressed")
            break #This should work, because only when the first fun reaches break, will the second loop be reached
        time.sleep(0.05)
    while True:
        if color == "red":
            print("broke")
            break
        tankFun(20, 0.1)
        print("rolled")
        
    
    #ToDo: Step 3: Rotate around until distance to next house is ca. 80cm
    

def buttonFun():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug

def tankFun(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)


def colorFun():
    global color
    color = "none"
    rawColor = colorSensor.color
    while True:
        if rawColor == 5:
            color = "red"
        elif rawColor == 3:
            color = "green"
        #return color
        print("color: " + str(rawColor))
        time.sleep(0.1)


if __name__=="__main__":
    main()