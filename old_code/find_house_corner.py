#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyroSensor = GyroSensor(INPUT_2)


def detectJumpInDist(threshold, dist)
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        time.sleep(0.005)
        distNew = ultraSoundSensor.distance_centimeters
        if distOld < 50:
            if abs(distOld-distNew) >= threshold:
                print("sees edge")
                #now it drives forwarda little bit and then turns 90° sees motor docs for that turning with pid