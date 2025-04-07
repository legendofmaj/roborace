#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound


studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)
#or: mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
#tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
# gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
speaker = Sound()
#tankDrive.gyro = gyroSensor

stop_event = threading.Event()

col_raw = [0, 0, 0]
tbdDistance = 10
dist = 0.0
circleAngle = 90
rightCornerDist = 0.0
leftCornerDist = 0.0
rightCornerAngle = 0
leftCornerAngle = 0
anOfAprch = 0.0
seesGreen = False
seesRed = False

anglesAndDists = {1000000 : 1000000}

posO = 90
zero = 90
Angle = 0



# def readCircleAngle(stop_event):
#     global circleAngle
#     while not stop_event:
#         circleAngle = gyroSensor.circle_angle()
#         Angle = gyroSensor.angle
#         time.sleep(0.05)
#         print(str(circleAngle) + "                                  " + str(Angle))

def getAngle():
    global posO
    #global Angle
    temp = (circleAngle - posO) + 90
    if temp < 0:
        return temp + 360
    elif temp > 360:
        return temp - 360
    else:
        return temp
    
# def readAngle():
#     global Angle
#     while True:
#         Angle = gyroSensor.angle
#         time.sleep(0.05)
#         print(Angle)

def main():
    #circleAngleThread =  threading.Thread(target=readCircleAngle(stop_event))
    #circleAngleThread.start()
    #anglethread = threading.Thread(target=readAngle)
    #anglethread.start()
    gyroSensor = GyroSensor(INPUT_2)
    tankDrive.on(SpeedPercent(-10), SpeedPercent(10))
    Time = 0
    while Time < 1:
        circleAngle = gyroSensor.circle_angle()
        Angle = gyroSensor.angle
        time.sleep(0.05)
        print(str(circleAngle) + "                                  " + str(Angle))
        time.sleep(0.1)
        Time += 1
    tankDrive.off()
    try:
        gyroSensor.reset()
    except:
        print("huh")
        pass
    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    Time = 0
    while Time < 1:
        circleAngle = gyroSensor.circle_angle()
        Angle = gyroSensor.angle
        time.sleep(0.05)
        print(str(circleAngle) + "                                  " + str(Angle))
        time.sleep(0.1)
        Time += 1
    tankDrive.off()
    #stop_event.set()
    #circleAngleThread.join()

if __name__ == "__main__":
    main()