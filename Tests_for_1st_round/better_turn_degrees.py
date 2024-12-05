#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedPercent
from ev3dev2.wheel import EV3EducationSetTire

import time

studmm = 7
studs_that_wheels_are_apart = 15


mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

def betterTurnDegrees(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)
    mdiff.odometry_stop()

#example usage
def main():
    betterTurnDegrees(90, 20)
    time.sleep(1)
    betterTurnDegrees(-90, 20)

if __name__=="__main__":
    main()