#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import turning

#Outputs and Inputs of the robot
leftMotorOutput = OUTPUT_C
rightMotorOutput = OUTPUT_B
depositMotorOutput = OUTPUT_A
rotationTowardHouse = 50
turnSpeed = 15


depositMotor = MediumMotor(depositMotorOutput)
leftMotor = LargeMotor(leftMotorOutput)
rightMotor = LargeMotor(rightMotorOutput)
tankDrive = MoveTank(leftMotorOutput, rightMotorOutput)
gyro = GyroSensor(INPUT_2)

#example usage
def main():
    #Rotate toward the current house
    turning.turnRightToX(rotationTowardHouse, turnSpeed)
    time.sleep(0.5)
    #drop the packet
    drop()
    time.sleep(0.5)

def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.75)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.75)
    

if __name__=="__main__":
    main()
