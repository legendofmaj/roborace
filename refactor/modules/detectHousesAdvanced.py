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

#import modules.newParallelWallDriveUsingColorCheck
from modules.anglesDistsThread import *
from modules.turning import *
from modules.parallelWallDrive import *

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)

stop_event = threading.Event()

col_raw = [
    0,
    0,
    0
]
tbdDistance = 10
dist = 0.0
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

#determine how to get to next house
def detectHouseEdge(threshold):
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
        distOld = modules.anglesDistsThread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = modules.anglesDistsThread.threadOutput.dist
        print(distNew)
        if distNew > 0:
            if abs(distOld-distNew) >= threshold:
                time.sleep(0.1)
                distNew = modules.anglesDistsThread.threadOutput.dist
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
        distOld = modules.anglesDistsThread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = modules.anglesDistsThread.threadOutput.dist
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
    posO = modules.anglesDistsThread.threadOutput.circleAngle
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
        detectHouseEdge(12)
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

def getHousesAdvanced(threshold):
    #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = modules.anglesDistsThread.threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turnLeftToX(150, 10)
    dist_at_oneOFive = modules.anglesDistsThread.threadOutput.dist
    edges = {900 : [1000, 1]}
    while getAngle() < 350 and getAngle() > 100:
        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo")
            break
        global anglesAndDists
        #see if house
        print("seing houses")
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
        tankDrive.off()
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))

        angleOld = getAngle()
        distOld = modules.anglesDistsThread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = modules.anglesDistsThread.threadOutput.dist
        print(distNew)

        if (distOld - distNew) < 0 and abs(distOld - distNew) >= threshold:
            print("dist jump further, left edge")
            #print(distOld)#debug
            #print(distNew)#debug
            leftCornerAngle = angleOld
            leftCornerDist = distOld + 10
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            edges[leftCornerAngle] = [leftCornerDist, 2]
            leftTurn(5, 10)
            print("lil turn")

        elif (distOld - distNew) > 0 and abs(distOld - distNew) >= threshold:
            print("dist jump closer, right edge")
            time.sleep(0.1)
            distNew = modules.anglesDistsThread.threadOutput.dist
            tankDrive.on(SpeedPercent(0), SpeedPercent(0))
            #print(distOld)#debug
            #print(distNew)#debug
            rightCornerAngle = angleNew
            rightCornerDist = distNew + 10
            print(rightCornerAngle)#debug
            print(rightCornerDist)#debug
            edges[rightCornerAngle] = [rightCornerDist, 1]
            leftTurn(5, 10)
            print("lil turn")

        else:
            print("passes")
            if getAngle() > 350 or getAngle() < 50:
                print("broke in passing")
                break
            continue

    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)
    leftest_edge = edges[edges_keys[0]]
    if leftest_edge[1] == 2:
        edges[150] = [dist_at_oneOFive, 1]
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)

    #def find_angles():
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)
    leftest_edge = edges[edges_keys[0]]
    if leftest_edge[1] == 2:
        edges[150] = [dist_at_oneOFive, 1]
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)

    for x in range(len(edges)):
        if x % 2 != 0:
            continue
        right = edges[edges_keys[x]]
        left = edges[edges_keys[(x+1)]]
        a = int(right[0])#rightCornerDist 
        b = int(left[0])#leftCornerDist 
        alpha = int(edges_keys[x])#rightCornerAngle
        beta = int(edges_keys[(x+1)])#leftCornerAngle
        anOfAprch = getAngleOfApproach(a, b, alpha, beta)
        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)
        anglesAndDists[int(distToNextHouse)] = int(anOfAprch)
        print(left)
        print(right)
        print(alpha)
        print(beta)
        print(anglesAndDists)
        print(x)

    edges.clear()
    edges_keys.clear()

    time.sleep(1)
    leftTurn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(5)
    tankDrive.off()

    turnRightToX(150, 10)
    print("turned back")
    time.sleep(1)
    toRemove = []
    for x in anglesAndDists:
        print("checking dists")
        print(x, anglesAndDists[x])
        turnLeftToX((anglesAndDists[x] + 90), 10)
        print("turning to angle")
        time.sleep(1)
        seenDist = modules.anglesDistsThread.threadOutput.dist
        if seenDist > (x-10) + 10 or seenDist < (x-10) - 10:
            print("doesnt think its right")
            toRemove.append(x)
    for x in toRemove:
        anglesAndDists.pop(x)
    toRemove.clear()

    time.sleep(0.2)

    print("checked angles and dist")