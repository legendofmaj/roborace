#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor

leftMotorOutput = OUTPUT_A
rightMotorOutput = OUTPUT_B
depositMotorOutput = OUTPUT_C
turnSpeed = 15

depositMotor = MediumMotor(OUTPUT_A)
leftMotor = LargeMotor(leftMotorOutput)
rightMotor = LargeMotor(rightMotorOutput)
tankDrive = MoveTank(leftMotorOutput, rightMotorOutput)
gyro = GyroSensor(INPUT_2)

def leftTurn(degrees):
    angle = gyro.circle_angle()
    startAngle = angle
    while abs(angle) < (startAngle + degrees):
        tankDrive.on(SpeedPercent(-turnSpeed), SpeedPercent(turnSpeed))
        angle = gyro.circle_angle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees):
    angle = gyro.circle_angle()
    startAngle = angle
    while abs(angle) < (startAngle + degrees):
        tankDrive.on(SpeedPercent(turnSpeed), SpeedPercent(-turnSpeed))
        angle = gyro.circle_angle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))