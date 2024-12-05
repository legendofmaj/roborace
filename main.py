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
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)
#or: moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

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
Angle = 90

time.sleep(0.3)

def main():
    
    print("please press")
    #play tone
    global seesRed
    global seesGreen

    startThreads()
    global zero
    zero = circleAngle

    Sound().play_file('/home/robot/ev3/miscellaneous/soundFiles/Audio1.wav', volume=100, play_type=0)
    
    while True:
       if Button().any() == True:
           break
       time.sleep(0.05)
    global posO
    
    global Angle
    posO = circleAngle
    zero = 90
    Angle = 90

    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
    time.sleep(0.5)
    #figure out how to detect an adge and drive parallel to a wall and see red
    while True:
        if seesRed == True:
            print("red")
            tankDrive.off()   
            seesRed = False

            posO = circleAngle
            
            getMultipleHouses()

            #add the dists to a list and sort it
            distsToNextHouse = anglesAndDists.keys()
            print(distsToNextHouse, anglesAndDists.keys())
            distsToNextHouse = [int(x) for x in distsToNextHouse]
            distsToNextHouse = sorted(distsToNextHouse)
            print(distsToNextHouse)
            #figure out which one is the shortest and save it, also figure out which is the correspaonding angle and save it
            try:
                shortestDist = int(distsToNextHouse[0])
                wantedAnOfAprch = int(float(anglesAndDists[shortestDist]))
            except IndexError:
                print("sorting distances: index error")

            #drop abd 
            #betterTurnLeftToX(180, 10)
            turnRightToX(40, 10)
            drop()
            time.sleep(0.5)
            print("checking dists")
            turnLeftToX((wantedAnOfAprch + 90), 10)
            print("turning to angle")
            time.sleep(0.5)
            seenDist = dist
            print(seenDist)
            time.sleep(0.2)

            turnRightToX(wantedAnOfAprch + 5, 5)
            #moveDifferential.turn_right(85, 7)

            toDriveDist = seenDist - 13
            if toDriveDist > 5:
                driveTillDistWheel(toDriveDist)
                print("drove")
            
            #moveDifferential.turn_left(10, 90)
            leftTurn(90, 10)
            time.sleep(0.2)
            seesRed = False
            tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.5)
            posO = circleAngle

            #then drive to thew next house and then turn  
        
        if seesGreen == True: 
            tankDrive.off()
            seesGreen = False
            print("green")
            smoothDriveStraight(20)
            time.sleep(3)
            tankDrive.off()
            break
        
        adjustDist_findEdge(17, 4, 10, 20, (0.9*22.3))

def startThreads():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)#, args=(stop_event))
    circleAngleThread.start()

def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

def readColor():
    global color
    global col_raw
    global seesGreen
    global seesRed
    color = "none"
    rawColor = colorSensor.color
    col_raw = colorSensor.raw
    while True:
        rawColor = colorSensor.color
        col_raw = colorSensor.raw
        if rawColor == 5:
            color = "red"
            seesRed = True
        elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            color = "green"
            seesGreen = True
        time.sleep(0.1)

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)

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

    
def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.75)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.75)


def adjustDist_findEdge(desired_dist, tolerance, speed, threshold, drive_further):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    #threshold, drive_further = 35, 22.3
    correct = 0
    if dist > desired_dist  + tolerance:
        print("dist too big")
        correct = 1
    elif dist < desired_dist - tolerance:
        print("dist too small")
        correct = -1
    elif dist > desired_dist - tolerance and dist < desired_dist + tolerance:
        correct = 0
        print("distance is correct")
    tankDrive.off()
    if correct == 1: #it starts turning outwards for some rteason and doesnt turn abcjk in
        distOld = dist
        #moveDifferential.turn_right(10, 4)
        rightTurn(4, 10)
        tankDrive.off()
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.15) 
        #distOld = dist
        #time.sleep(0.5)
        tankDrive.off()
        #moveDifferential.turn_left(10, 4)
        leftTurn(4, 10)
        tankDrive.off() 
        distNew = dist
    if correct == -1:
        distOld = dist
        #moveDifferential.turn_left(10, 5)
        leftTurn(4, 10)
        tankDrive.off()
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.15)
        #distOld = dist
        #time.sleep(0.5)
        tankDrive.off()
        #moveDifferential.turn_right(10, 4)
        rightTurn(4, 10)
        tankDrive.off()
        distNew = dist
        #print("hello is past second turn")
    if correct == 0:
        distOld = dist
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.15)
        distNew = dist
    if distOld != 0:
        if abs(distOld-distNew) >= threshold: # this works best when it dosnt need to turn first otherwise might seen an edge where ther isnt one
            print("sees edge")
            rotations = 0.00
            while True:
                rotation = 0.9
                tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), rotation)
                rotations += rotation
                dist_crossed = rotations * 22.3 #in cm
                if dist_crossed >= drive_further:
                    tankDrive.off()
                    break

            #moveDifferential.turn_right(10, 85) #should be ninety overturns tho
            rightTurn(85, 10)
            #tankDrive.off()
            time.sleep(0.5)
            tankDrive.on(SpeedPercent(0), SpeedPercent(0))
            time.sleep(0.1)
            tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.5) #this works very inconsistently
            tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.5)
            time.sleep(0.5)
            print(getAngle())
            #tankDrive.off()
            time.sleep(0.5)
            global posO
            posO = circleAngle
            print(getAngle())
            time.sleep(0.5)

#driving
def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDistWheel(dist):
    #tankDrive.on(SpeedPercent(-5), SpeedPercent(-5))
    rotations = 0.00
    rotation = 0.01
    while True:
        tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), rotation)
        rotations += rotation
        dist_crossed = rotations * 22.3 #in cm
        if dist_crossed >= dist:
            break

#turning
def betterTurnRightToX(degrees, speed):
    moveDifferential.odometry_start()
    moveDifferential.turn_to_angle(SpeedPercent(speed), degrees)
    moveDifferential.odometry_stop()

def betterTurnLeftToX(degrees, speed):
    moveDifferential.odometry_start()
    moveDifferential.turn_to_angle(SpeedPercent(-speed), degrees)
    moveDifferential.odometry_stop()

def leftTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle < min(350,(startAngle + degrees)):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = getAngle()
        if angle > 350:
            break
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

#moveDifferential.turn_left(SpeedPercent(speed), degrees)

def rightTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle > max((startAngle - degrees), 10):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
        if angle < 10:#if it slightly overturns at a 90°turn from ninety degrees
            break
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

#moveDifferential.turn_right(SpeedPercent(speed), degrees)

def turnRightToX(degrees, speed):
    angle = getAngle()
    while angle > max(10, degrees - 5):
        #moveDifferential.turn_right(speed, 1)
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = getAngle()
    while angle < min(degrees + 5, 350):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        #moveDifferential.turn_left(speed, 1)
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

#determine how to get to next house
def detectHouseEdges(threshold):
    #betterTurnRightToX(7, 7)
    print("seeking")
    global rightCornerAngle
    global leftCornerAngle
    global rightCornerDist
    global leftCornerDist
    tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
    while True:
        if getAngle() > 350 or getAngle() < 50:
            tankDrive.off()
            break
        angleOld = getAngle()
        distOld = dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = dist
        print(distNew)
        if distNew > 0:
            if abs(distOld-distNew) >= threshold:
                time.sleep(0.1)
                distNew = dist
                tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                rightCornerAngle = angleNew
                rightCornerDist = distNew + 10
                print(rightCornerAngle)#debug
                print(rightCornerDist)#debug
                break
    print("found one")#debug
    tankDrive.off()
    time.sleep(1)
    #betterTurnDegrees(5, 15)
    if getAngle() < 350 and getAngle() > 150:
        #moveDifferential.turn_left(10, 5)
        leftTurn(5, 10)
        print("lil turn")
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
        
    while True:
        if getAngle() > 350 or getAngle() < 50:
            break
        #this here so it doesnt get stuck indefinitly executing
        angleOld = getAngle()
        distOld = dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = dist
        print(distNew)
        if abs(distOld-distNew) >= threshold:
            leftCornerAngle = angleOld
            leftCornerDist = distOld + 10
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            break
    tankDrive.off()
    print("right Corner Angle: " + str(rightCornerAngle)  + ", right Corner distance: " + str(rightCornerDist)) #debug
    print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug

def getMultipleHouses():
    
    #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turnLeftToX(150, 10) #turn so that the sensor points outwards
    print("turned outwards")
    time.sleep(0.5)
    while getAngle() < 350 and getAngle() > 100:
        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo")
            break
        global anglesAndDists
        #see if house
        print("seing houses")
        detectHouseEdges(12)
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
        tankDrive.off()
        print("saw houses")
        
        a = rightCornerDist 
        b = leftCornerDist 
        alpha = rightCornerAngle
        beta = leftCornerAngle

        anOfAprch = getAngleOfApproach(a, b, alpha, beta)

        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)

        anglesAndDists[int(distToNextHouse)] = int(anOfAprch)

        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo2")
            break

        time.sleep(1)
        #moveDifferential.turn_left(5, 10)
        leftTurn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(5)
    tankDrive.off()

    turnRightToX(150, 10)
    print("turned back")
    time.sleep(1)

    print("checked angles and dist")
        
def getAngleOfApproach(a, b, alpha, beta):
    global anOfAprch
    try:
        anOfAprch = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
    except ZeroDivisionError:
        anOfAprch = 90
        print("Angle of Approach calculation: zero division error")
    except:
        print("Angle of Approach calculation: unknown error")
    return anOfAprch

def getDistToNextHouse(a, alpha, anOfAprch):
    distToNextHouse = abs(math.cos(anOfAprch - alpha)) * a
    return distToNextHouse

if __name__=="__main__":
    main()