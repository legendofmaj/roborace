#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor
from ev3dev2.button import Button

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
tankDrive.gyro = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
gyroSensor = GyroSensor(INPUT_2)



def __init__():
    distThread = threading.Thread(target= read_dist)
    distThread.start()

def read_button():
    buttonPressed = False
    while True:
        if Button().any() == True:
            buttonPressed = True
            return buttonPressed
        
def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.01)



def detectJumpInDist(threshold, dist):
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        time.sleep(0.005)
        distNew = ultraSoundSensor.distance_centimeters
        if distOld < 50:
            if abs(distOld-distNew) >= threshold:
                print("sees edge")
                rotations = 0.00
                while True:
                    tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), 0.01)
                    rotations += 0.01
                    dist_crossed = rotations* 22.3 #in cm
                    if dist_crossed >= dist:
                        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                        #circleAngle = gyroSensor.circle_angle()
                        break
                tankDrive.turn_degrees(SpeedPercent(5), -90) 
                # turns 90° sees motor docs for that turning with pid