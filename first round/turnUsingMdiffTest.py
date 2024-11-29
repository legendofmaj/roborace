#!/usr/bin/env python3

import time
import threading 
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveDifferential, SpeedPercent
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.sound import Sound




studmm = 8
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

STUD_MM = 7
gyroSensor = GyroSensor(INPUT_2)
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, 15 * STUD_MM)
posO = 90
circleAngle = 90




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

def turnToAngle(speed, degrees):
    # Enable odometry
    mdiff.odometry_start()

    # Use odometry to rotate in place to 90 degrees
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)

    # Disable odometry
    mdiff.odometry_stop()

def turnRightToX(degrees, speed):
    angle = getAngle()
    while angle > degrees - 5:
        mdiff.turn_right(10, 1)
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = getAngle()
    while angle < degrees + 5:
        #tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        mdiff.turn_left(10, 1)
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)

def main():
    circleAngleThread = threading.Thread(target = readCircleAngle)#, args=(stop_event))
    circleAngleThread.start()
    # Rotate 90 degrees clockwise
    mdiff.turn_right(SpeedPercent(10), 90)
    time.sleep(1)
    mdiff.turn_left(SpeedPercent(10), 90)
    time.sleep(2)
    #turnToAngle(10, 180)
    turnLeftToX(180, 10)
    print("got here")

if __name__=="__main__":
    main()