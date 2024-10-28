#!/usr/bin/env python3
# "master"

import time
import sys
import threading


#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor


#Define mconstants
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
btn = Button()
colorSensor = ColorSensor(INPUT_1)
uSoundSensor = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)

#Define variables
seesRed = False
seesGreen = False
consoleInput = "undefined"
dist = 0.0



def main():
    print("Enter moveTank to test basic tank steering")
    print("Enter drop to test the drop motor")
    threading1 = threading.Thread(target=readInputAndAct)
    threading1.start()
    while True:
        if btn.any():
            print("Button pressed!") 
        if consoleInput == "moveTank":
            moveTank(3)
        elif consoleInput == "drop":
            drop() 
        #else:
            #print("invalid input")  
        readColor()
        if seesRed == True:
            drop() #code muss am ende so sein dass der rober es nicht dauerhaft wiederholt also nur erneut ausführt wenn er erneut rot sieht nachdem er erst etwas anderes gesehen hat
        if seesGreen == True:
            moveTank(1)
            break
        readDist()
        readCircleAngle()
        time.sleep(1)

    print("saw green so stopped")
        

def moveTank(timeIn):
    global consoleInput
    #Move the tank
    seconds = timeIn
    print("moving") #debug
    tankDrive.on_for_seconds(SpeedPercent(-50), SpeedPercent(-50), seconds)
    consoleInput = "undefined"


def drop():
    global consoleInput
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.9)
    consoleInput = "undefined"


def readInputAndAct():
    while True:
        global consoleInput
        time.sleep(1)
        print("seeking") #debug
        userInput = input()
        print("input:" + userInput) #debug
        consoleInput = userInput


def readColor():
    global seesRed
    global seesGreen
    colorDetected = colorSensor.color
    #print(colorSensor.rgb) #debug
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


def readDist():
    global dist
    dist = uSoundSensor.distance_centimeters
    #print("distance: " + str(dist)) #debug
    #sometimes values seem larger than thy are if the sensor is angled towards a surface


def readCircleAngle():
    global circleAngle
    circleAngle = gyro.circle_angle() # starts at 90° when turned right by 90°goes to 360°; when rotated by 180° goes to 270°; when rotated by 270° to the right goes to 180°; when rotated by 360° to the right goes back to 90°
    #print("circle angle: " + str(circleAngle)) # debug
    #this acts stange here, showing the same value even tho the rotation of the robot is changed



if __name__ =="__main__":
    main()