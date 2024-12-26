#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire

#import modules.modultwo
import modules.turning
from modules.anglesDistsThread import *

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def getHousePrimitive():
    global dist_short
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    modules.turning.turntoxl(150, 10)
    dist_short = 1000
    angle_short = 180
    while getAngle() < 350 and getAngle() > 100:
        tankDrive.on(SpeedPercent(-5), SpeedPercent(5))
        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo")
            break
        distOld = threadOutput.dist
        time.sleep(0.1)
        distNew = threadOutput.dist
        angleNew = threadOutput.circleAngle
        if distOld > distNew:
            if dist_short > distNew:
                dist_short = distNew
                angle_short = angleNew
    global anglesAndDists
    anglesAndDists = {int(dist_short) : int(angle_short)}