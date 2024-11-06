#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import turning

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
    turning.rightTurn(rotationTowardHouse)
    time.sleep(0.5)
    #drop the packet
    drop()
    #Rotate back to position of origin
    time.sleep(0.5)
    turning.leftTurn(rotationTowardHouse)



if __name__=="__main__":
    main()
