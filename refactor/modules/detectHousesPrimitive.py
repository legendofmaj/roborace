#!/usr/bin/env python3

import time
import threading 
import sys
import math

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire

#import modules.modultwo
import modules.turning
from modules.anglesDistsThread import *

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def getHousePrimitive():
    global dist_short
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    modules.turning.turntoxl(150, 10)
    dist_short = 1000
    angle_short = 180
    while getAngle() < 350 and getAngle() > 100:
        tankDrive.on(SpeedPercent(-5), SpeedPercent(5))
        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo")
            break
        distOld = threadOutput.dist
        time.sleep(0.1)
        distNew = threadOutput.dist
        angleNew = threadOutput.circleAngle
        if distOld > distNew:
            if dist_short > distNew:
                dist_short = distNew
                angle_short = angleNew
    global anglesAndDists
    anglesAndDists = {int(dist_short) : int(angle_short)}



def getHousesNew(threshold):
    #global rightCornerAngle
    #global leftCornerAngle
    #global rightCornerDist
    #global leftCornerDist
    #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    #gyroSensor.reset()
    global posO
    posO = circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turnLeftToX(150, 10)
    dist_at_oneOFive = dist
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
        distOld = dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = dist
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
            distNew = dist
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

    '''for x in range(len(edges)):
        right = edges[edges_keys[x]]
        left = edges[edges_keys[(x+1)]]
        a = right[0]#rightCornerDist 
        b = left[0]#leftCornerDist 
        alpha = edges[edges_keys[x]]#rightCornerAngle
        beta = edges[edges_keys[(x+1)]]#leftCornerAngle
        anOfAprch = getAngleOfApproach(a, b, alpha, beta)
        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)
        anglesAndDists[int(distToNextHouse)] = int(anOfAprch)
        x += 1'''
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
    '''if getAngle() > 350 or getAngle() < 50:
            print("broke in multo2")
            break'''


    '''print("checking")
        
    a = rightCornerDist 
    b = leftCornerDist 
    alpha = rightCornerAngle
    beta = leftCornerAngle

    anOfAprch = getAngleOfApproach(a, b, alpha, beta)

    distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)

    anglesAndDists[int(distToNextHouse)] = int(anOfAprch)'''

        

    time.sleep(1) #there was an unexpected indentation error here
        #mdiff.turn_left(5, 10)
        #leftTurn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(5)
    tankDrive.off()

    turnRightToX(150, 10)
    print("turned back")
    time.sleep(1)
    '''toRemove = []
    for x in anglesAndDists:
        print("checking dists")
        print(x, anglesAndDists[x])
        betterTurnLeftToX((anglesAndDists[x] + 90), 10)
        print("turning to angle")
        time.sleep(1)
        seenDist = dist
        if seenDist > (x-10) + 10 or seenDist < (x-10) - 10:
            print("doesnt think its right")
            toRemove.append(x)
    for x in toRemove:
        anglesAndDists.pop(x)
    toRemove.clear()'''

    print("checked angles and dist")