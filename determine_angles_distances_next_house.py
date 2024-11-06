#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from turning import leftTurn

leftMotor = LargeMotor(OUTPUT_C)
rightMotor = LargeMotor(OUTPUT_B)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)


def main():
    print("beginning")
    detectDistJumpAngle(20)


def detectDistJumpAngle(threshold):
    gyro.reset() #testing
    print("seeking")
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        #print(distOld)
        leftTurn(1, 10)
        distNew = ultraSoundSensor.distance_centimeters
        if distNew < 100:
            if abs(distOld-distNew) >= threshold:
                print(distOld)#debug
                print(distNew)#debug
                rightCornerAngle = gyro.circle_angle()
                rightCornerDist = distNew
                print(rightCornerAngle)#debug
                print(rightCornerDist)#debug
                break
    print("found one")#debug
    time.sleep(1)
    leftTurn(1, 10)
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        #print(distOld)
        leftTurn(1, 10)
        distNew = ultraSoundSensor.distance_centimeters
        if abs(distOld-distNew) >= threshold:
            print(distOld)#debug
            print(distNew)#debug
            leftCornerAngle = gyro.circle_angle()
            leftCornerDist = distOld
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            break
    print("right Corner Angle: " + str(rightCornerAngle)+ ", right Corner distance: " + str(rightCornerDist)) #debug
    print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug

if __name__=="__main__":
    main()