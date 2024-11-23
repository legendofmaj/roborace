#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

leftMotor = LargeMotor(OUTPUT_C)
rightMotor = LargeMotor(OUTPUT_B)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

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

def turnRightToX(degrees, speed):
    angle = gyro.circle_angle()
    while angle > degrees:
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = gyro.circle_angle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = gyro.circle_angle()
    while angle < (degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = gyro.circle_angle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
