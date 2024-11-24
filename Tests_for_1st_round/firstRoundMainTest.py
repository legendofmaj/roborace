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
from ev3dev2.wheel import EV3Tire

STUD_MM = 8
speed = 15
studs_that_wheels_are_apart = 16
mm_that_wheels_are_apart = 128
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, studs_that_wheels_are_apart * STUD_MM)
#Alternative: mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, mm_that_wheels_are_apart)

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

col_raw = [0, 0, 0]
tbdDistance = 10
dist = 0.0
circleAngle = 90
rightCornerDist = 0.0
leftCornerDist = 0.0
rightCornerAngle = 0
leftCornerAngle = 0
anOfAprch = 0.0



def __init__threads__():
    gyroSensor.reset()
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    buttonThread = threading.Thread(target = readButton)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    angleThread = threading.Thread(target = readAngle)
    angleThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)
    circleAngleThread.start()

####        
def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)


def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug

def readColor():
    global color
    global col_raw
    color = "none"
    rawColor = colorSensor.color
    col_raw = colorSensor.raw
    while True:
        rawColor = colorSensor.color
        col_raw = colorSensor.raw
        if rawColor == 5:
            color = "red"
        elif rawColor == 3:
            color = "green"
        time.sleep(0.1)

def readAngle():
    global circleAngle
    while True:
        angle = gyroSensor.angle
        time.sleep(0.05)

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
####


 



def main():
    if __name__ == __init__threads__:
        __init__threads__()

    print("u may press")
    #play tone

    while True:
        if buttonPressed == True:
            print("pressed")
            break
        time.sleep(0.05)

    #figure out how to detect an adge and drive parallel to a wall and see red
 
    if color == "red":
        tankDrive.off   
        detectHouseEdges(35) 

        a = rightCornerDist
        b = leftCornerDist
        alpha = rightCornerAngle
        beta = leftCornerAngle

        anOfAprch = getAngleOfApproach(a, b, alpha, beta)

        turnLeftToX(anOfAprch, 10)
        #drop abd then drive to thew next house and then turn

    

    while True:
        if (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            break
        smoothDriveStraight(20)
        time.sleep(3)
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    




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
#sensors




#driving
def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distance): #this doesnt work anymore
    while True:
        if dist <= distance:
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug

def driveTillDistWheel(dist):
    #tankDrive.on(SpeedPercent(-5), SpeedPercent(-5))
    rotations = 0.00
    while True:
        tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), 0.01)
        rotations += 0.01
        dist_crossed = rotations* 22.3 #in cm
        if dist_crossed >= dist:
            break



#turning
def betterTurnDegrees(degrees):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedRPM(speed), degrees)
    mdiff.odometry_stop()
def leftTurn(degrees, speed):
    angle = circleAngle
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = circleAngle
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    angle = circleAngle
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = circleAngle
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnRightToX(degrees, speed):
    angle = circleAngle
    while angle > degrees:
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = circleAngle
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = circleAngle
    while angle < degrees:
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = circleAngle
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))


#dropping
def drop():
    turnRightToX(50, 15)
    time.sleep(0.5)
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.9)
    time.sleep(0.5)


#determine how to get to next house
def detectHouseEdges(threshold):
    gyroSensor.reset()
    print("seeking")
    global rightCornerAngle
    global leftCornerAngle
    global rightCornerDist
    global leftCornerDist
    tankDrive.on(SpeedPercent(-5), SpeedPercent(5))
    while True:
        angleOld = circleAngle
        distOld = dist
        time.sleep(0.05)
        angleNew = circleAngle
        distNew = dist
        if distNew < 100:
            if abs(distOld-distNew) >= threshold:
                tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                print(distOld)#debug
                print(distNew)#debug
                rightCornerAngle = angleNew
                rightCornerDist = distNew
                print(rightCornerAngle)#debug
                print(rightCornerDist)#debug
                break
    print("found one")#debug
    tankDrive.off
    time.sleep(1)
    betterTurnDegrees(5):
    tankDrive.on(SpeedPercent(-5), SpeedPercent(5))
    while True:
        angleOld = circleAngle
        distOld = dist
        time.sleep(0.005)
        angleNew  =circleAngle
        distNew = dist
        if abs(distOld-distNew) >= threshold:
            print(distOld)#debug
            print(distNew)#debug
            leftCornerAngle = angleOld
            leftCornerDist = distOld
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            break
    tankDrive.off
    print("right Corner Angle: " + str(rightCornerAngle)+ ", right Corner distance: " + str(rightCornerDist)) #debug
    print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug

def getAngleOfApproach(a, b, alpha, beta):
    global anOfAprch
    anOfAprch = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
    return anOfAprch

if __name__=="__main__":
    main()