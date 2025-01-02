#!/usr/bin/env python3

#reads out values of angles and dists using threads

import time
import threading 

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

#class containing measured values
class threadOutput:         ### a class is used as this allows current values to be exported
    circleAngle = 90
    Angle = 0
    dist = 17

#function to start the threads and thus start measuring
def startThreads():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)
    circleAngleThread.start()

#function to read distance
def read_dist():
    while True:
        threadOutput.dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)
#function to read circleAngle and Angle (2 different things)
def readCircleAngle():
    while True:
        threadOutput.circleAngle = gyroSensor.circle_angle()
        threadOutput.Angle = gyroSensor.angle
        time.sleep(0.05)
# function to get the relative circleangle compared to a start circleangle
def getRelAnglev(spos):
    temp = threadOutput.circleAngle - spos
    return temp
# impromptu function to "reset" the value of circleangle to its out-the-box value (90°)
def getAngle(posO):
    temp = (threadOutput.circleAngle - posO) + 90
    return temp%360

#function to get the delta in angle compared to a start angle
def getRelAngle(spos):
    temp = threadOutput.Angle - spos
    return temp