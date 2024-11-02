#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor


btn = Button()
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)


dist = 0.0


def main():
    print("start") #debug
    buttonThread = threading.Thread(target= readButton)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target= readColor)
    colorThread.start()
    distThread = threading.Thread(target= readDist)
    distThread.start()
    print("threads on") #debug
    while True:
        if buttonPressed == True:
            print("button pressed") #debug
            break #This should work, because only when the first fun reaches break, will the second loop be reached
        time.sleep(0.05)
    while True:
        if color == "red":
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug
        
    
    #ToDo: Step 3: Rotate around until distance to next house is ca. 80cm
    

def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug


def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)


def readColor():
    global color
    color = "none"
    rawColor = colorSensor.color
    while True:
        rawColor = colorSensor.color
        if rawColor == 5:
            color = "red"
        elif rawColor == 3:
            color = "green"
        #return color
        print("color: " + str(rawColor)) #debug
        time.sleep(0.1)


def readDist():
    global dist
    while True:
        dist = ultraSoundSensor.distance_centimeters #distance in centimeters
        time.sleep(0.1)


def driveTillDist(distance): #this might also be replaced by calculating the distance per wheel rotation and rotationg the wheel based on that
    while True:
        if dist <= distance:
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug


if __name__=="__main__":
    main()