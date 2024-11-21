#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, LargeMotor, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

import time
import threading 
import sys
import math

#Input and Output list
ultrasound_sensor_port = INPUT_3
gyro_sensor_port = INPUT_2
rightMotor = OUTPUT_B
leftMotor = OUTPUT_C

tank_drive = MoveTank(leftMotor, rightMotor)
ultrasound_sensor = UltrasonicSensor(ultrasound_sensor_port)
gyro = GyroSensor(gyro_sensor_port)
tank_drive.gyro = GyroSensor(INPUT_2)

desired_dist = 15
dist = 0

def main():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    time.sleep(1)
    #while True:
    #    if read_button() == True:
    #        break
    while True:
        global dist
        print(dist) #debug only
        detectJumpInDist(35)
        adjust_dist(desired_dist, 4, 20)


def read_button():
    buttonPressed = False
    while True:
        if Button().any() == True:
            buttonPressed = True
            return buttonPressed
        
def read_dist():
    while True:
        global dist 
        dist = ultrasound_sensor.distance_centimeters
        time.sleep(0.01)
        #return dist #this might make it too inaccurate
    
def drive(speed):
    tank_drive.on(SpeedPercent(-speed), SpeedPercent(-speed)) #Replace with -speed on real robot

'''def check_dist(desired_dist, tolerance):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    if dist > desired_dist  + tolerance:
        print("dist too big")
        correct = 1
    elif dist < desired_dist - tolerance:
        print("dist too small")
        correct = -1
    elif dist > desired_dist - tolerance and dist < desired_dist + tolerance:
        correct = 0
    return correct'''

def adjust_dist(desired_dist, tolerance, speed):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    if dist > desired_dist  + tolerance:
        print("dist too big")
        correct = 1
    elif dist < desired_dist - tolerance:
        print("dist too small")
        correct = -1
    elif dist > desired_dist - tolerance and dist < desired_dist + tolerance:
        correct = 0
    tank_drive.off
    if correct == 1:
        tank_drive.turn_degrees(SpeedPercent(speed), -4)
        tank_drive.on(SpeedPercent(-speed), SpeedPercent(-speed)) 
        #time.sleep(0.2) 
    if correct == -1:
        tank_drive.turn_degrees(SpeedPercent(-speed), 4) 
        tank_drive.on(SpeedPercent(-speed), SpeedPercent(-speed))
        #time.sleep(0.2)
    if correct == 0:
        tank_drive.on(SpeedPercent(-speed), SpeedPercent(-speed))
        #time.sleep(0.1)

def detectJumpInDist(threshold):
    #distThread = threading.Thread(target= readDist)
    #distThread.start()
    #while True:
    distOld = dist
    time.sleep(0.005)
    distNew = dist
    if distOld < 50:
        if abs(distOld-distNew) >= threshold:
            print("sees edge")
            rotations = 0.00
            while True:
                tank_drive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), 0.01)
                rotations += 0.01
                dist_crossed = rotations* 22.3 #in cm
                if dist_crossed >= dist:
                    tank_drive.off
                        #circleAngle = gyroSensor.circle_angle()
                    break
            tank_drive.turn_degrees(SpeedPercent(5), -90) 
                # turns 90° sees motor docs for that turning with pid
def readDist():
    while True:
        global dist
        dist = ultrasound_sensor.distance_centimeters

detectJumpInDist(35)