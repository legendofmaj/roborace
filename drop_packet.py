#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor

#Please test these values!
#Outputs and Inputs of the robot (please change for actual robot, I couldn't figure out how to change this in the simulation)
leftMotorOutput = OUTPUT_A
rightMotorOutput = OUTPUT_B
depositMotorOutput = OUTPUT_C
rotationTowardHouse = 50
turnSpeed = 15


depositMotor = MediumMotor(OUTPUT_A)
leftMotor = LargeMotor(leftMotorOutput)
rightMotor = LargeMotor(rightMotorOutput)
tankDrive = MoveTank(leftMotorOutput, rightMotorOutput)
gyro = GyroSensor(INPUT_2)


def main():
    #Rotate toward the current house
    rightTurn(rotationTowardHouse)
    #drop the packet
    depositMotor.on_for_rotations(SpeedPercent(75), 2.25)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -2.25)
    time.sleep(0.5)
    #Rotate back to position of origin
    leftTurn(rotationTowardHouse)

def leftTurn(degrees):
    angle = gyro.circle_angle()
    startAngle = angle
    while abs(angle) > (startAngle + degrees):
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

if __name__=="__main__":
    main()
