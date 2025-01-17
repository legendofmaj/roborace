#!/usr/bin/env python3
"""reads out values of angles and dists using threads"""

import time
import threading
import dataclasses

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

@dataclasses.dataclass
class ThreadOutput:
    """class containing measured values
    a class is used as this allows current values to be exported"""
    circle_angle = 90
    angle = 0
    dist = 17

def start_threads():
    """function to start the threads and thus start measuring"""
    dist_thread = threading.Thread(target= read_dist)
    dist_thread.start()
    circle_angle_thread = threading.Thread(target = read_circle_angle)
    circle_angle_thread.start()

def read_dist():
    """function to read distance"""
    while True:
        ThreadOutput.dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

def read_circle_angle():
    """function to read circleAngle and Angle (2 different things)"""
    while True:
        ThreadOutput.circleAngle = gyroSensor.circle_angle()
        ThreadOutput.Angle = gyroSensor.angle
        time.sleep(0.05)

def get_relative_angle(spos):
    """function to get the relative circleangle compared to a start circleangle"""
    temp = ThreadOutput.circleAngle - spos
    return temp

def get_angle(pos_o):
    """impromptu function to "reset" the value of circleangle to its out-the-box value (90°)"""
    temp = (ThreadOutput.circleAngle - pos_o) + 90
    return temp%360

def get_rel_angle(spos):
    """function to get the delta in angle compared to a start angle"""
    temp = ThreadOutput.Angle - spos
    return temp
# End-of-file (EOF)
