#!/usr/bin/env python3


from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

def driveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distIn):
    while True:
        distInt = ultraSoundSensor.distance_centimeters
        if distInt <= distIn:
            break
        driveStraight(20)
    driveStraight(0)