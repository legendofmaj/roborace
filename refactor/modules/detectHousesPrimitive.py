"""this module is a very primitive way to determine at which angle and distance the next house is"""
#seems to be the most reliable if most unelegant and unprecise approach
#if houses are present which do not match the given geometric perameters for a target house they will still be driven at

#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

import modules.turning
from modules.anglesDistsThread import *

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)


# this works after a very simple priciple: it is assumed that the shortest distance is the most direct way to the next house, so the robot sweeps around once and  then remembers the shortest distance and the angle at which it was located and saves this into a dict which it then returns
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
    return anglesAndDists