#!/usr/bin/env python3

import time
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedPercent
from ev3dev2.wheel import EV3EducationSetTire

STUD_MM = 8

mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, 15 * STUD_MM)




def turnToAngle(speed, degrees):
    # Enable odometry
    mdiff.odometry_start()

    # Use odometry to rotate in place to 90 degrees
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)

    # Disable odometry
    mdiff.odometry_stop()

def main():
    # Rotate 90 degrees clockwise
    mdiff.turn_right(SpeedPercent(20), 90)
    time.sleep(1)
    mdiff.turn_left(SpeedPercent(20), 90)
    turnToAngle(20, 60)

if __name__=="__main__":
    main()