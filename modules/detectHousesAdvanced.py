#!/usr/bin/env python3

#two more approaches to find the next house

import time
import threading 
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound

from angles_dists_thread import *
from turning import *
from parallelWallDrive import *

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

#determine how to get to next house this is the simpler of the two, but struggles if a house wall is going beyont the 150° arc in which it looks 
# #this will only find one house and it will assume that the right edge of the house is to the left of the current angle of the robot
def detectHouseEdge(threshold):
    print("seeking")
    global rightCornerAngle
    global leftCornerAngle
    global rightCornerDist
    global leftCornerDist
    tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
    while True:                                                 ###turns until it finds a jump in the measured distance
        if getAngle() > 350 or getAngle() < 50:
            tankDrive.off()
            break
        angleOld = getAngle()
        distOld = angles_dists_thread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = angles_dists_thread.threadOutput.dist
        print(distNew)
        if distNew > 0:
            if abs(distOld-distNew) >= threshold:                       ###here it checks for the jump and if it finds one it will save its location
                time.sleep(0.1)
                distNew = angles_dists_thread.threadOutput.dist
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
    if getAngle() < 350 and getAngle() > 150:                           ###turns a little bit to prevent the same edge from being seen twice
        #moveDifferential.turn_left(10, 5)
        left_turn(5, 10)
        print("lil turn")
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
        
    while True:                                                 ###turns until it finds a jump in the measured distance
        if getAngle() > 350 or getAngle() < 50:
            break
        #the above is here so it doesnt get stuck indefinitly executing
        angleOld = getAngle()
        distOld = angles_dists_thread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = angles_dists_thread.threadOutput.dist
        print(distNew)
        if abs(distOld-distNew) >= threshold:               ###here it checks for the jump and if it finds one it will save its location
            leftCornerAngle = angleOld
            leftCornerDist = distOld + 10
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            break
    tankDrive.off()
    print("right Corner Angle: " + str(rightCornerAngle)  + ", right Corner distance: " + str(rightCornerDist)) #debug
    print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug


#this function serves to combine multiple of the detectHouseEdge functions int o one function to find all houses and determine the next house
def getMultipleHouses():
    
    #drive forward about 1x the length of the robot from the color sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = angles_dists_thread.threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turn_left_to_x(150, 10) #turn so that the sensor points outwards
    print("turned outwards")
    time.sleep(0.5)
    while getAngle() < 350 and getAngle() > 100: ###executes the detectHouesEdge function over and over again until it finds all houses in its given arc
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

        anOfAprch = getAngleOfApproach(a, b, alpha, beta) ###uses the getAngleOfApproach function to determine the angle of approach

        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch) ###uses the getDistToNextHouse function to determine the distance to the detected house

        anglesAndDists[int(distToNextHouse)] = int(anOfAprch) ###saves both those values into a dict

        if getAngle() > 350 or getAngle() < 50:
            print("broke in multo2")
            break

        time.sleep(1)
        left_turn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(5)
    tankDrive.off()

    turn_right_to_x(150, 10)
    print("turned back")
    time.sleep(1)

    print("checked angles and dist")

#uses trigonometry to find the angle of approach to the next house whereasin the angle of approach represents the orthogonal line from the house wall to the robots axis of rotation
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

#uses simple trigonometry to find the distance to the next house (aka length of the orthogonal)
def getDistToNextHouse(a, alpha, anOfAprch):
    distToNextHouse = abs(math.cos(anOfAprch - alpha)) * a
    return distToNextHouse


#this function is a more advance version of the combination of the above 4 functions
#it accouts for what type of edge it detects and has the ability to determine if a house is actually a valid target for delivery
def getHousesAdvanced(threshold):
    #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(getAngle())
    tankDrive.off()
    time.sleep(0.5)
    global posO
    posO = angles_dists_thread.threadOutput.circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turn_left_to_x(150, 10)
    dist_at_oneOFive = angles_dists_thread.threadOutput.dist
    edges = {900 : [1000, 1]}
    while getAngle() < 350 and getAngle() > 100: ###begins turning to find the houses
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
        distOld = angles_dists_thread.threadOutput.dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = angles_dists_thread.threadOutput.dist
        print(distNew)

        if (distOld - distNew) < 0 and abs(distOld - distNew) >= threshold: ###this is a left edge as the newer distance(to the left of the wall) is longer than the distance to the wall
            print("dist jump further, left edge")
            #print(distOld)#debug
            #print(distNew)#debug
            leftCornerAngle = angleOld
            leftCornerDist = distOld + 10
            print(leftCornerAngle)#debug
            print(leftCornerDist)#debug
            edges[leftCornerAngle] = [leftCornerDist, 2]
            left_turn(5, 10)
            print("lil turn")

        elif (distOld - distNew) > 0 and abs(distOld - distNew) >= threshold: ###this is a right adge as the distance gets shorter
            print("dist jump closer, right edge")
            time.sleep(0.1)
            distNew = angles_dists_thread.threadOutput.dist
            tankDrive.on(SpeedPercent(0), SpeedPercent(0))
            #print(distOld)#debug
            #print(distNew)#debug
            rightCornerAngle = angleNew
            rightCornerDist = distNew + 10
            print(rightCornerAngle)#debug
            print(rightCornerDist)#debug
            edges[rightCornerAngle] = [rightCornerDist, 1]
            left_turn(5, 10)
            print("lil turn")

        else:
            print("passes")
            if getAngle() > 350 or getAngle() < 50:
                print("broke in passing")
                break
            continue

    ###sorts the edges according to angle
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)
    leftest_edge = edges[edges_keys[0]]
    if leftest_edge[1] == 2:
        edges[150] = [dist_at_oneOFive, 1] ### if the leftest edge is a left one it sets the value at 150°(the start angle) as the new leftest edge
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)

    for x in range(len(edges)):###determines the angles of approach and the distances to all the houses it finds
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
    left_turn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(5)
    tankDrive.off()

    turn_right_to_x(150, 10) ###turns back to the start angle
    print("turned back")
    time.sleep(1)
    toRemove = []
    for x in anglesAndDists: ###goes through all the angles of approach and their corresponding distances and compares them to the actual distance. if the decrepancy is to big it assumes the house its currently looking at is not a valid house to deliver to
        print("checking dists")
        print(x, anglesAndDists[x])
        turn_left_to_x((anglesAndDists[x] + 90), 10)
        print("turning to angle")
        time.sleep(1)
        seenDist = angles_dists_thread.threadOutput.dist
        if seenDist > (x-10) + 10 or seenDist < (x-10) - 10:
            print("doesnt think its right")
            toRemove.append(x)
    for x in toRemove:   ###removes invalid houses
        anglesAndDists.pop(x)
    toRemove.clear()

    time.sleep(0.2)

    print("checked angles and dist")