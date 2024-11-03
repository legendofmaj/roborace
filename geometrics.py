#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

leftMotor = LargeMotor(OUTPUT_A)
rightMotor = LargeMotor(OUTPUT_B)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)

def main():
    ninetyDegreeTurn()
    maxValRight()
    #Figure out how far the robot has turned ToDo: The current implementation using timePassed is very poor and should be fixed
    returnToMiddle()
    maxValLeft()

def ninetyDegreeTurn():
    #While this function does seem to work, it is by no means pretty and should be replaced with a proper function asap
    rightMotor.on_for_rotations(SpeedPercent(25), 1.4)

def maxValRight():
    prev = float('-inf')
    threshold = 25
    global timePassed
    timePassed = 0

    while True:
        leftMotor.on(SpeedPercent(10))
        dist = ultraSoundSensor.distance_centimeters
        #print(dist - prev) #debug
        if abs(dist - prev) > threshold and abs(dist - prev) < 5000: #the 5000 is there to not register the infinity value
            print("Success") #debug
            leftMotor.on(SpeedPercent(0))
            break
        prev = dist
        time.sleep(0.1)
        timePassed = timePassed + 0.1

def returnToMiddle():
    rightMotor.on_for_seconds(SpeedPercent(10), timePassed)

def maxValLeft():
    prev = float('-inf')
    threshold = 25

    while True:
        rightMotor.on(SpeedPercent(10))
        dist = ultraSoundSensor.distance_centimeters
        #print(dist - prev) #debug
        if abs(dist - prev) > threshold and abs(dist - prev) < 5000: #the 5000 is there to not register the infinity value
            print("Success") #debug
            rightMotor.on(SpeedPercent(0))
            break
        prev = dist
        time.sleep(0.1)

if __name__=="__main__":
    main()