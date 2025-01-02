#!/usr/bin/env python3
"""This module is a very primitive way to determine at which angle and distance the next house is"""
#Additional notes:
#seems to be the most reliable if most unelegant and unprecise approach.
#if houses are present which do not match the given geometric parameters
#for a target house they will still be driven at


import time

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

import turning
from angles_dists_thread import ThreadOutput, get_angle

STUD_MM = 7
STUDS_THAT_WHEELS_ARE_APART = 15
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, STUDS_THAT_WHEELS_ARE_APART * STUD_MM)

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)


def get_house_primitive():
    """ this works after a very simple priciple: it is assumed that the shortest distance is the 
    most direct way to the next house, so the robot sweeps around once and  then remembers the 
    shortest distance and the angle at which it was located and saves this into a dict which it 
    then returns"""
    tank_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tank_drive.off()
    print(get_angle())
    tank_drive.off()
    time.sleep(0.5)
    print(get_angle())
    time.sleep(0.5)
    print("driven")
    turning.turn_to_x_left(150, 10)
    dist_short = 1000
    angle_short = 180
    while get_angle() < 350 and get_angle() > 100:
        tank_drive.on(SpeedPercent(-5), SpeedPercent(5))
        if get_angle() > 350 or get_angle() < 50:
            print("broke in multo")
            break
        dist_old = ThreadOutput.dist
        time.sleep(0.1)
        dist_new = ThreadOutput.dist
        angle_new = ThreadOutput.circle_angle
        if dist_old > dist_new:
            if dist_short > dist_new:
                dist_short = dist_new
                angle_short = angle_new
    angles_and_dists = {int(dist_short) : int(angle_short)}
    return angles_and_dists
# End-of-file (EOF)
