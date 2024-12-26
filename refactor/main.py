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

# #import modules.newParallelWallDriveUsingColorCheck
# import modules.test_detect_houses
# import modules.modultwo
# import modules.oldParallelWallDrive

from modules.anglesDistsThread import *
import modules.parallelWallDrive
import modules.detectHousesPrimitive
import modules.turning

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
gyroSensor = GyroSensor(INPUT_2)

stop_event = threading.Event()

col_raw = [0, 0, 0]
tbdDistance = 10
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

time.sleep(0.3)

def main():
    
    print("please press")
    #play tone
    global seesRed
    global seesGreen

    startThreads()
    global zero
    zero = threadOutput.circleAngle

    Sound().play_file('/home/robot/ev3/miscellaneous/soundFiles/Audio1.wav', volume=100, play_type=0)
    
    while True:
        if Button().any() == True:
           break
        time.sleep(0.05)
    global posO
    posO = threadOutput.circleAngle
    zero = 90

    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
    time.sleep(0.5)
    color = [False, False, False]
    while True:
        color = modules.parallelWallDrive.main()
        if color[1] == True:
            print("red")
            tankDrive.off()   
            seesRed = False

            posO = threadOutput.circleAngle
            
            modules.detectHousesPrimitive.getHousePrimitive()

            wantedAnOfAprch = int(float(modules.detectHousesPrimitive.anglesAndDists[modules.detectHousesPrimitive.dist_short]))
            
            modules.turning.turntoxr(50, 10)
            drop()
            time.sleep(0.5)
            print("checking dists")
            modules.turning.turntoxl((wantedAnOfAprch + 90), 10)
            print("turning to angle")
            time.sleep(0.5)
            seenDist = threadOutput.dist
            print(seenDist)
            time.sleep(0.2)
            modules.turning.turntoxr(wantedAnOfAprch, 10)

            toDriveDist = seenDist - 13
            if toDriveDist > 5:
                driveTillDistWheel(toDriveDist)
                print("drove")
            
            modules.turning.relturnv(90, 10)
            time.sleep(0.2)
            seesRed = False
            posO = threadOutput.circleAngle
        
        if color[2] == True: 
            tankDrive.off()
            seesGreen = False
            print("green")
            smoothDriveStraight(20)
            time.sleep(3)
            tankDrive.off()
            break

    
def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.75)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.75)


#driving
def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDistWheel(dist):
    rotations = 0.00
    rotation = 0.01
    while True:
        tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), rotation)
        rotations += rotation
        dist_crossed = rotations * 22.3 #in cm
        if dist_crossed >= dist:
            break


if __name__=="__main__":
    main()