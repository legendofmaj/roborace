#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound




studmm = 8
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)
#or: mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
#tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
speaker = Sound()
#tankDrive.gyro = gyroSensor

stop_event = threading.Event()

col_raw = [0, 0, 0]
tbdDistance = 10
dist = 0.0
circleAngle = 90
rightCornerDist = 0.0
leftCornerDist = 0.0
rightCornerAngle = 0
leftCornerAngle = 0
anOfAprch = 0.0
seesGreen = False
seesRed = False

anglesAndDists = {1000000 : 1000000}

posO = 90
Angle = 90



def main():

    startThreads()

    global posO
    posO = circleAngle

    time.sleep(1)
    print(getAngle())
    betterTurnLeftToX(180, 10)
    time.sleep(1)
    print(getAngle())
    posO = circleAngle
    print(getAngle())

    betterTurnRightToX(0, 10)

    print(getAngle())


def startThreads():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    buttonThread = threading.Thread(target = readButton)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    #angleThread = threading.Thread(target = readAngle)
    #angleThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)#, args=(stop_event))
    circleAngleThread.start()

def startingFanfare():
    speaker.play_song([('C4',500), ('F4',250), ('C4',250)])#to be played before starting to navigate thru course

def finishFanfare():
    speaker.play_song([('C4', 400), ('E4', 400), ('G4', 400), ('B4', 400), ('G4', 400), ('B4', 650)])#to be played after finishing course


def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

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
    global col_raw
    global seesGreen
    global seesRed
    color = "none"
    rawColor = colorSensor.color
    col_raw = colorSensor.raw
    while True:
        rawColor = colorSensor.color
        col_raw = colorSensor.raw
        if rawColor == 5:
            color = "red"
            seesRed = True
            #print("aw yep red")
        #elif rawColor == 3:
        #    color = "green"
        elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            color = "green"
            seesGreen = True
        time.sleep(0.1)

def readAngle():
    #global angle
    while True:
     #   angle = gyroSensor.angle
        time.sleep(0.05)

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)

def getAngle():
    global posO
    #global Angle
    temp = (circleAngle - posO) + 90
    if temp < 0:
        return temp + 360
    elif temp > 360:
        return temp - 360
    else:
        return temp




def betterTurnRightToX(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(-speed), degrees)
    mdiff.odometry_stop()

def betterTurnLeftToX(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)
    mdiff.odometry_stop()
    
def leftTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle <= (startAngle + degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle >= max((startAngle - degrees), 0):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
        if angle > 350 and angle <= 360:#if it slightly overturns at a 90°turn from ninety degrees
            break
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnRightToX(degrees, speed):
    angle = getAngle()
    while angle > degrees:
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = getAngle()
    while angle < degrees:
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

main()