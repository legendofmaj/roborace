#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedPercent
from ev3dev2.wheel import EV3EducationSetTire, EV3Tire




#calculate distance between wheels (I don't really know which measurement is correct. This is just taken from mathStuff)
min_dist_between_wheels = 118 #mm
studmm = 8
studs_that_wheels_are_apart = 15


mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)
#or: MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

def betterTurnDegrees(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)
    mdiff.odometry_stop()

#example usage
def main():
    betterTurnDegrees(90)

if __name__=="__main__":
    main()