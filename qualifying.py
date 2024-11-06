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
import driving
import drop_packet
import turning
import determine_angles_distances_next_house


btn = Button()
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

#To be changed variables for testing
tbdDistance = 5


dist = 0.0
circleAngle = 90

def main():
    startThreads()

    #Start driving when any button on the ev3 is pressed
    while True:
        if buttonPressed == True:
            break
        time.sleep(0.05)

    #Drive until the red line is reached
    while True:
        if color == "red":
            break
        driving.driveStraight(20, 0.1)

    #determine geometrics
    determine_angles_distances_next_house.main()

    #Drop the package
    drop_packet.main()    


    #get angle of approach
    #turn toward house

    #Drive until a tbd distance to the next house and turn by 90° degrees
    driving.driveTillDist(tbdDistance)
    turning.leftTurn(90)

    #Drive until the green line is reached
    while True:
        if color == "green":
            break
        driving.driveStraight(20, 0.1)
    
    
def startThreads():
    buttonThread = threading.Thread(target = readButton)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    distThread = threading.Thread(target = readDist)
    distThread.start()
    angleThread = threading.Thread(target = readCircleAngle)
    angleThread.start()

def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug

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

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circleAngle()
        time.sleep(0.05)

if __name__=="__main__":
    main()