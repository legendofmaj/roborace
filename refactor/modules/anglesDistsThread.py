#!/usr/bin/env python3

import time
import threading 

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

class threadOutput:
    circleAngle = 90
    Angle = 0
    dist = 17

def startThreads():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)
    circleAngleThread.start()

def read_dist():
    while True:
        threadOutput.dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

def readCircleAngle():
    while True:
        threadOutput.circleAngle = gyroSensor.circle_angle()
        threadOutput.Angle = gyroSensor.angle
        time.sleep(0.05)

def getRelAnglev(spos):
    temp = threadOutput.circleAngle - spos
    return temp

def getAngle(posO):
    temp = (threadOutput.circleAngle - posO) + 90
    return temp%360

def getRelAngle(spos):
    temp = threadOutput.Angle - spos
    return temp