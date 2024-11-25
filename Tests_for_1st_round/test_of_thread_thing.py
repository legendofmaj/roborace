#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.wheel import EV3Tire, EV3EducationSetTire# i think the latter tire is the one we are using

import time
import threading 
import sys
import math


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
tankDrive.gyro = gyroSensor

circleAngle = 90
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

stop_event = threading.Event()

gyroSensor.reset()
tankDrive.gyro.reset()

def readCircleAngle():
    global circleAngle
    while not stop_event.is_set():
    #while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)
    print("is set")

def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug

def main():
    print("y tho")
    buttonThread = threading.Thread(target = readButton)
    buttonThread.daemon = True
    buttonThread.start()
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.5)
    while True:
        print("asdfgnmsdfghjm,")
        circleAngleThread = threading.Thread(target = readCircleAngle)#d, args=(stop_event, ))
        circleAngleThread.start()

        print(circleAngle)

        gyroSensor.reset()
        tankDrive.gyro.reset()

        tankDrive.turn_degrees(SpeedPercent(-10), 90)

        time.sleep(1)

        tankDrive.turn_degrees(SpeedPercent(-10), -90)

        stop_event.set()
        circleAngleThread.join()
        gyroSensor.reset()
        tankDrive.gyro.reset()
        time.sleep(1)

        tankDrive.turn_degrees(SpeedPercent(-10), 90)

        time.sleep(1)

        tankDrive.turn_degrees(SpeedPercent(-10), -90)

        stop_event.clear()
        circleAngleThread = threading.Thread(target = readCircleAngle)
        circleAngleThread.start()

        tankDrive.turn_degrees(SpeedPercent(-10), 90)

        time.sleep(1)

        tankDrive.turn_degrees(SpeedPercent(-10), -90)
        if buttonPressed == True:
            print("pressed")
            break

if __name__=="__main__":
    main()