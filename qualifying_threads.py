#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound

btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
speaker = Sound()

#To be changed variables for testing
col_raw = [0, 0, 0]
tbdDistance = 15
dist = 0.0
circleAngle = 90
rightCornerDist = 0.0
leftCornerDist = 0.0
rightCornerAngle = 0
leftCornerAngle = 0
anOfAprch = 0.0
volume = 100

gyroSensor.reset()

def main():
    startThreads()
    print("u may press")

    #Start driving when any button on the ev3 is pressed
    #while True:
        #if buttonPressed == True:
    print("pressed")
            #break
        #time.sleep(0.05)

    #Drive until the red line is reached
    while True:
        if color == "red":
            print("saw red")
            break
        print("driving")
        smoothDriveStraight(10)
    smoothDriveStraight(0)
    #determine geometrics
    detectDistJumpAngle(15)

    #Drop the package
    drop()   


    #get angle of approach (not yet finished)
    #Debugging Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
    a = rightCornerDist
    b = leftCornerDist
    alpha = rightCornerAngle
    beta = leftCornerAngle

    anOfAprch = getAngleOfApproach(a, b, alpha, beta)

    #turn toward house
    turnLeftToX(anOfAprch, 10)
    #Drive until a tbd distance to the next house and turn by 90° degrees
    driveTillDist(tbdDistance)
    leftTurn(90)

    #Drive until the green line is reached
    while True:
        if (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            break
        smoothDriveStraight(20)
        time.sleep(3)
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
        print("done")
        speaker.play_tone(220, 1, 0.1, volume, play_type=0)
        speaker.play_tone(180, 1, 0.1, volume, play_type=0)
        speaker.play_tone(140, 3, 2, volume, play_type=0)
    
    
def startThreads():
    #buttonThread = threading.Thread(target = readButton)
    #buttonThread.daemon = True
    #buttonThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    distThread = threading.Thread(target = readDist)
    distThread.start()
    angleThread = threading.Thread(target = readCircleAngle)
    angleThread.start()

def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug


#sensors
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
        #return color
        #print("color: " + str(rawColor)) #debug
        time.sleep(0.1)

def readDist():
    global dist
    while True:
        dist = ultraSoundSensor.distance_centimeters #distance in centimeters
        time.sleep(0.1)

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)


#driving
def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distance): #this might also be replaced by calculating the distance per wheel rotation and rotationg the wheel based on that
    while True:
        if dist <= distance:
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug

def smoothDriveTillDist(distance):
    while True:
        if dist <= distance:
            break
        smoothDriveStraight(20)
    smoothDriveStraight(0)


#turning
def leftTurn(degrees, speed):
    #print(gyro.circle_angle())
    angle = circleAngle
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = circleAngle
        #print(angle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    #print(gyro.circle_angle())
    angle = circleAngle
    startAngle = angle
    while angle < (startAngle + degrees):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = circleAngle
        #print(angle)
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
def detectDistJumpAngle(threshold):
    print("seeking")
    tankDrive.on(SpeedPercent(-10), SpeedPercent(10))
    while True:
        distOld = dist
        #print(distOld)
        #leftTurn(1, 10)
        time.sleep(0.005)
        distNew = dist
        if distNew < 100:
            if abs(distOld-distNew) >= threshold:
                print(distOld)#debug
                print(distNew)#debug
                rightCornerAngle = circleAngle
                rightCornerDist = distNew
                print(rightCornerAngle)#debug
                print(rightCornerDist)#debug
                break
    print("found one")#debug
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    time.sleep(10)#make 1 later
    leftTurn(3, 10)
    tankDrive.on(SpeedPercent(-10), SpeedPercent(10))
    while True:
        distOld = dist
        #print(distOld)
        #leftTurn(1, 10)
        time.sleep(0.005)
        distNew = dist
        if abs(distOld-distNew) >= threshold:
            print(distOld)#debug
            print(distNew)#debug
            leftCornerAngle = circleAngle
            leftCornerDist = distOld
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            break
    tankDrive.on(SpeedPercent(-10), SpeedPercent(10))
    print("right Corner Angle: " + str(rightCornerAngle)+ ", right Corner distance: " + str(rightCornerDist)) #debug
    print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug

def getAngleOfApproach(a, b, alpha, beta):
    global anOfAprch
    anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
    

if __name__=="__main__":
    main()