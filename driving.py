#!/usr/bin/env python3


from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from qualifying import distance

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distIn): #this might also be replaced by calculating the distance per wheel rotation and rotationg the wheel based on that
    distInt = ultraSoundSensor.distance_centimeters
    while True:
        if distInt <= distIn:
            print("broke") #debug
            print(distInt)
            break
        driveStraight(20, 0.1)
        distInt = ultraSoundSensor.distance_centimeters
        print("rolled") #debug

def smoothDriveTillDist(distIn):
    while True:
        distInt = ultraSoundSensor.distance_centimeters
        if distInt <= distIn:
            break
        smoothDriveStraight(20)
    smoothDriveStraight(0)