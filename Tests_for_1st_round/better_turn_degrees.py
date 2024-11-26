#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedPercent
from ev3dev2.wheel import EV3EducationSetTire, EV3Tire

#variables
mm_that_wheels_are_apart = 0

#calculate distance between wheels (I don't really know which measurement is correct. This is just taken from mathStuff)
min_dist_between_wheels = 118 #mm
max_dist_between_wheels = 188 #mm
min_dist_to_middle = 59 #mm
max_dist_to_middle = 94 #mm
mm_that_wheels_are_apart = (min_dist_to_middle + max_dist_to_middle)/2

mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)

def betterTurnDegrees(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)
    mdiff.odometry_stop()

#example usage
def main():
    betterTurnDegrees(90)

if __name__=="__main__":
    main()