#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_2
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor

gyro = GyroSensor(INPUT_2)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def turnRightToX(degrees, speed):
    angle = gyro.circle_angle()
    while angle > degrees:
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = gyro.circle_angle()
    tankDrive.off()

def turnLeftToX(degrees, speed):
    angle = gyro.circle_angle()
    while angle < (degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = gyro.circle_angle()
    tankDrive.off()