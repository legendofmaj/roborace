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

desired_dist = 20
dist = 0
distOld = 0
distNew = 0

def main():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    edgeThread = threading.Thread(target = detectEdge)
    edgeThread.start()
    time.sleep(1)
    global distOld
    global distNew
    while True:

        #detectJumpInDist(35, 22.3)
        
        adjust_dist(desired_dist, 4, 10)
        drive(10)

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

def adjust_dist(desired_dist, tolerance, speed, threshold, drive_further):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    #print("jeah no")
    #global distOld
    #threshold, drive_further = 35, 22.3
    if dist > desired_dist  + tolerance:
        print("dist too big")
        correct = 1
    elif dist < desired_dist - tolerance:
        print("dist too small")
        correct = -1
    elif dist > desired_dist - tolerance and dist < desired_dist + tolerance:
        correct = 0
        print("hmm sees to be right")
    tank_drive.off
    if correct == 1:
        distOld = dist
        tank_drive.turn_degrees(SpeedPercent(-speed), 5)
        tank_drive.off
        tank_drive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.01) 
        distOld = dist
        #time.sleep(0.5)
        tank_drive.off
        tank_drive.turn_degrees(SpeedPercent(-speed), -5)
        tank_drive.off 
        distNew = dist
    if correct == -1:
        distOld = dist
        tank_drive.turn_degrees(SpeedPercent(-speed), -4) 
        tank_drive.off
        tank_drive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.01)
        distOld = dist
        #time.sleep(0.5)
        tank_drive.off
        #print("gets herd")
        tank_drive.turn_degrees(SpeedPercent(-speed), 4)
        tank_drive.off
        distNew = dist
        #print("hello is past second turn")
    if correct == 0:
        distOld = dist
        tank_drive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.01)
        distNew = dist
        #time.sleep(0.3)
    if distOld < 50:
        if abs(distOld-distNew) >= threshold:
            print("sees edge")
            rotations = 0.00
            while True:
                rotation = 1
                tank_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), rotation)
                rotations += rotation
                dist_crossed = rotations* 22.3 #in cm
                if dist_crossed >= drive_further:
                    tank_drive.off
                    break
            tank_drive.turn_degrees(SpeedPercent(-10), 90) 
                    # turns 90° sees motor docs for that turning with pid

def detectEdge():
    
    global distOld
    global distNew
    while True:
        distOld = dist
        time.sleep(0.5)
        distNew = dist
        #print("arrived in detect edge")
        if distOld < 50:
            if abs(distOld-distNew) >= threshold:
                print("sees edge")
                rotations = 0.00
                while True:
                    tank_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
                    rotations += 1
                    dist_crossed = rotations* 22.3 #in cm
                    if dist_crossed >= drive_further:
                        tank_drive.off
                        break
                tank_drive.turn_degrees(SpeedPercent(-10), 90) 
                    # turns 90° sees motor docs for that turning with pid
    
def readDist():
    while True:
        global dist
        dist = ultrasound_sensor.distance_centimeters

if __name__ == "__main__":
    main()