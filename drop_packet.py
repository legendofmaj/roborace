#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor
from turning import turnXDegreesLeft, turnXDegreesRight

#Please test these values!
#Outputs and Inputs of the robot (please change for actual robot, I couldn't figure out how to change this in the simulation)
leftMotorOutput = OUTPUT_C
rightMotorOutput = OUTPUT_B
depositMotorOutput = OUTPUT_A
rotationTowardHouse = 50
turnSpeed = 15


depositMotor = MediumMotor(OUTPUT_A)
leftMotor = LargeMotor(leftMotorOutput)
rightMotor = LargeMotor(rightMotorOutput)
tankDrive = MoveTank(leftMotorOutput, rightMotorOutput)
gyro = GyroSensor(INPUT_2)


def main():
    #Rotate toward the current house
    turnXDegreesRight(rotationTowardHouse, 15)
    #drop the packet
    drop()
    #Rotate back to position of origin
    turnXDegreesLeft(rotationTowardHouse, 15)

def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.9)
    time.sleep(0.5)

if __name__=="__main__":
    main()
