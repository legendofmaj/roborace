#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

leftMotor = LargeMotor(OUTPUT_C)
rightMotor = LargeMotor(OUTPUT_B)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def ninetyDegreeTurnLeft(): #inaccurate +-5degrees
    tankDrive.on_for_rotations(SpeedPercent(-15), SpeedPercent(15), 0.4999)

def ninetyDegreeTurnRight(): #inaccurate +-5degrees
    tankDrive.on_for_rotations(SpeedPercent(15), SpeedPercent(-15), 0.4999)

def ninetyDegreeTurnLeftSmart():
    print(gyro.circle_angle())
    angle = gyro.circle_angle()
    startAngle = angle
    while angle <= (startAngle + 90):
        tankDrive.on_for_rotations(SpeedPercent(-15), SpeedPercent(15), 0.01)
        angle = gyro.circle_angle()
        print(angle)

def ninetyDegreeTurnRightSmart():
    print(gyro.circle_angle())
    angle = gyro.circle_angle()
    startAngle = angle
    while angle >= (startAngle - 90) :
        tankDrive.on_for_rotations(SpeedPercent(15), SpeedPercent(-15), 0.01)
        angle = gyro.circle_angle()
        print(angle)

def leftTurn(degrees, speed):
    #print(gyro.circle_angle())
    angle = gyro.circle_angle()
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = gyro.circle_angle()
        #print(angle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    #print(gyro.circle_angle())
    angle = gyro.circle_angle()
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = gyro.circle_angle()
        #print(angle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))