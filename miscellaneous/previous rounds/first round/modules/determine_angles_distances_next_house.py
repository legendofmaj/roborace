#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

import turning

leftMotor = LargeMotor(OUTPUT_C)
rightMotor = LargeMotor(OUTPUT_B)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyroSensor = GyroSensor(INPUT_2)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def main():
    detectDistJumpAngle(15)

class importantValues:
    rightCornerDist = 0.0
    leftCornerDist = 0.0
    rightCornerAngle = 0
    leftCornerAngle = 0

def detectDistJumpAngle(threshold):
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        turning.turning.leftTurn(1, 10)
        distNew = ultraSoundSensor.distance_centimeters
        if distNew < 100:
            if abs(distOld-distNew) >= threshold:
                print(distOld)#debug
                print(distNew)#debug
                importantValues.rightCornerAngle = gyroSensor.circle_angle() 
                importantValues.rightCornerDist = distNew
                print(importantValues.rightCornerAngle)#debug
                print(importantValues.rightCornerDist)#debug
                break
    time.sleep(1)
    turning.leftTurn(1, 10)
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        turning.leftTurn(1, 10)
        distNew = ultraSoundSensor.distance_centimeters
        if abs(distOld-distNew) >= threshold:
            print(distOld)#debug
            print(distNew)#debug
            importantValues.leftCornerAngle = gyroSensor.circle_angle()
            importantValues.leftCornerDist = distOld
            print(importantValues.leftCornerAngle)#debug
            print(importantValues.leftCornerDist)#debug
            break
    print("right Corner Angle: " + str(importantValues.rightCornerAngle)+ ", right Corner distance: " + str(importantValues.rightCornerDist)) #debug
    print("left Corner Angle: " + str(importantValues.leftCornerAngle)+ ", left Corner distance: " + str(importantValues.leftCornerDist)) #debug


if __name__=="__main__":
    main()