"""This module is a very primitive way to determine at which angle and distance the next house is"""
#Additional notes:
#seems to be the most reliable if most unelegant and unprecise approach.
#if houses are present which do not match the given geometric parameters
#for a target house they will still be driven at

#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

import modules.turning
from modules.anglesDistsThread import threadOutput, getAngle

STUD_MM = 7
STUDS_THAT_WHEELS_ARE_APART = 15
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, STUDS_THAT_WHEELS_ARE_APART * STUD_MM)

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)


def get_house_primitive():
    """ this works after a very simple priciple: it is assumed that the shortest distance is the 
    most direct way to the next house, so the robot sweeps around once and  then remembers the 
    shortest distance and the angle at which it was located and saves this into a dict which it 
    then returns"""
    #global dist_short ?I'm not sure if this breaks anything
    tank_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tank_drive.off()
    print(getAngle())
    tank_drive.off()
    time.sleep(0.5)
    #global pos_0 ?I'm not sure if this breaks anything
    pos_0 = threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    modules.turning.turntoxl(150, 10)
    dist_short = 1000
    angle_short = 180
    while getAngle() < 350 and getAngle() > 100:
        tank_drive.on(SpeedPercent(-5), SpeedPercent(5))
        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo")
            break
        dist_old = threadOutput.dist
        time.sleep(0.1)
        dist_new = threadOutput.dist
        angle_new = threadOutput.circleAngle
        if dist_old > dist_new:
            if dist_short > dist_new:
                dist_short = dist_new
                angle_short = angle_new
    #global anglesAndDists ?I am not sure if this break anything
    anglesAndDists = {int(dist_short) : int(angle_short)}
    return anglesAndDists
# End-of-file (EOF)
