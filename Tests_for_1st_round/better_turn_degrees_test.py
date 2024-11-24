#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire

#variables
STUD_MM = 8
speed = 15
studs_that_wheels_are_apart = 16
mm_that_wheels_are_apart = 128

# Question: How far are the wheels apart? # found in mathy stuff in the folder for tests for qualifying
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, studs_that_wheels_are_apart * STUD_MM)
#Alternative: mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, mm_that_wheels_are_apart)

def betterTurnDegrees(degrees):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedRPM(speed), degrees)
    mdiff.odometry_stop()

#example usage
def main():
    betterTurnDegrees(90)

if __name__=="__main__":
    main()