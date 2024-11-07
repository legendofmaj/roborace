#!/usr/bin/env python3


from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from qualifying import distance

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distIn): #this might also be replaced by calculating the distance per wheel rotation and rotationg the wheel based on that
    while True:
        if distance.dist <= distIn:
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug

def smoothDriveTillDist(distIn):
    while True:
        if distance.dist <= distIn:
            break
        smoothDriveStraight(20)
    smoothDriveStraight(0)