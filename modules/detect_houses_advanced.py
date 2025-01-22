#!/usr/bin/env python3
"""This modules contains two more approaches to find the next house"""

import time
import threading
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

import angles_dists_thread
from turning import turn_left_to_x, left_turn, turn_right_to_x
#from parallel_wall_drive import *

STUDMM = 7
STUDS_THAT_WHEELS_ARE_APART = 15
MIN_DIST_BETWEEN_WHEELS = 118 #mm
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, STUDS_THAT_WHEELS_ARE_APART * STUDMM)

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
TBD_DISTANCE = 10
DIST = 0.0
RIGHT_CORNER_DIST = 0.0
LEFT_CORNER_DIST = 0.0
RIGHT_CORNER_ANGLE = 0
LEFT_CORNER_ANGLE = 0
ANGLE_OF_APPROACH = 0.0

angles_and_dists = {1000000 : 1000000}

POS_O = angles_dists_thread.ThreadOutput.circle_angle
ZERO = 90

def detect_house_edge(threshold):
    """determine how to get to next house. This is the simpler of the two, but struggles if a house wall is going beyond the 150° arc in which it looks."""
    #Note: this will only find one house and it will assume that the right edge of the house is to the left of the current angle of the robot
    print("seeking")
    global RIGHT_CORNER_ANGLE
    global LEFT_CORNER_ANGLE
    global RIGHT_CORNER_DIST
    global LEFT_CORNER_DIST
    tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
    while True:                                                 ###turns until it finds a jump in the measured distance
        if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
            tankDrive.off()
            break
        angle_old = angles_dists_thread.get_angle(POS_O)
        dist_old = angles_dists_thread.ThreadOutput.DIST
        print(dist_old)
        time.sleep(0.07)
        angle_new = angles_dists_thread.get_angle(POS_O)
        dist_new = angles_dists_thread.ThreadOutput.DIST
        print(dist_new)
        if dist_new > 0:
            if abs(dist_old-dist_new) >= threshold:                       ###here it checks for the jump and if it finds one it will save its location
                time.sleep(0.1)
                dist_new = angles_dists_thread.ThreadOutput.DIST
                tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                RIGHT_CORNER_ANGLE = angle_new
                RIGHT_CORNER_DIST = dist_new + 10
                print(RIGHT_CORNER_ANGLE)#debug
                print(RIGHT_CORNER_DIST)#debug
                break
    print("found one")#debug
    tankDrive.off()
    time.sleep(1)
    #betterTurnDegrees(5, 15)
    if angles_dists_thread.get_angle(POS_O) < 350 and angles_dists_thread.get_angle(POS_O) > 150:                           ###turns a little bit to prevent the same edge from being seen twice
        #moveDifferential.turn_left(10, 5)
        left_turn(5, 10)
        print("lil turn")
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))

    while True:                                                 ###turns until it finds a jump in the measured distance
        if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
            break
        #the above is here so it doesnt get stuck indefinitly executing
        angle_old = angles_dists_thread.get_angle(POS_O)
        dist_old = angles_dists_thread.ThreadOutput.DIST
        print(dist_old)
        time.sleep(0.07)
        angle_new = angles_dists_thread.get_angle(POS_O)
        dist_new = angles_dists_thread.ThreadOutput.DIST
        print(dist_new)
        if abs(dist_old-dist_new) >= threshold:               ###here it checks for the jump and if it finds one it will save its location
            LEFT_CORNER_ANGLE = angle_old
            LEFT_CORNER_DIST = dist_old + 10
            print(LEFT_CORNER_ANGLE)#debug
            print(LEFT_CORNER_DIST)#debug
            break
    tankDrive.off()
    print("right Corner Angle: " + str(RIGHT_CORNER_ANGLE)  + ", right Corner distance: " + str(RIGHT_CORNER_DIST)) #debug
    print("left Corner Angle: " + str(LEFT_CORNER_ANGLE)+ ", left Corner distance: " + str(LEFT_CORNER_DIST)) #debug


def get_multiple_houses():
    """this function serves to combine multiple of the detectHouseEdge functions int o one function to find all houses and determine the next house"""
    #drive forward about 1x the length of the robot from the color sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(angles_dists_thread.get_angle(POS_O))
    tankDrive.off()
    time.sleep(0.5)
    global POS_O
    POS_O = angles_dists_thread.ThreadOutput.DIST
    time.sleep(0.5)
    print(angles_dists_thread.get_angle(POS_O))
    time.sleep(0.5)
    print("driven")
    turn_left_to_x(150, 10) #turn so that the sensor points outwards
    print("turned outwards")
    time.sleep(0.5)
    while angles_dists_thread.get_angle(POS_O) < 350 and angles_dists_thread.get_angle(POS_O) > 100: ###executes the detectHouesEdge function over and over again until it finds all houses in its given arc
        if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
            print("broke in multo")
            break
        global angles_and_dists
        #see if house
        print("seing houses")
        detect_house_edge(12)
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
        tankDrive.off()
        print("saw houses")

        a = RIGHT_CORNER_DIST
        b = LEFT_CORNER_DIST
        alpha = RIGHT_CORNER_ANGLE
        beta = LEFT_CORNER_ANGLE

        ANGLE_OF_APPROACH = get_angle_of_appoach(a, b, alpha, beta) ###uses the get_angle_of_appoach function to determine the angle of approach

        dist_to_next_house = get_dist_to_next_house(a, alpha, ANGLE_OF_APPROACH) ###uses the get_dist_to_next_house function to determine the distance to the detected house

        angles_and_dists[int(dist_to_next_house)] = int(ANGLE_OF_APPROACH) ###saves both those values into a dict

        if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
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

    print("checked angles and DIST")


def get_angle_of_appoach(a, b, alpha, beta):
    """uses trigonometry to find the angle of approach to the next house whereasin the angle of approach represents the orthogonal line from the house wall to the robots axis of rotation"""
    global ANGLE_OF_APPROACH
    try:
        ANGLE_OF_APPROACH = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
    except ZeroDivisionError:
        ANGLE_OF_APPROACH = 90
        print("Angle of Approach calculation: ZERO division error")
    except:
        print("Angle of Approach calculation: unknown error")
    return ANGLE_OF_APPROACH

#uses simple trigonometry to find the distance to the next house (aka length of the orthogonal)
def get_dist_to_next_house(a, alpha, ANGLE_OF_APPROACH):
    dist_to_next_house = abs(math.cos(ANGLE_OF_APPROACH - alpha)) * a
    return dist_to_next_house


def get_houses_advanced(threshold):
    """this function is a more advance version of the combination of the above 4 functions"""
    #Note: it accouts for what type of edge it detects and has the ability to determine if a house is actually a valid target for delivery

    #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
    tankDrive.off()
    print(angles_dists_thread.get_angle(POS_O))
    tankDrive.off()
    time.sleep(0.5)
    global POS_O
    POS_O = angles_dists_thread.ThreadOutput.circle_angle
    time.sleep(0.5)
    print(angles_dists_thread.get_angle(POS_O))
    time.sleep(0.5)
    print("driven")
    turn_left_to_x(150, 10)
    dist_at_one_o_five = angles_dists_thread.ThreadOutput.DIST
    edges = {900 : [1000, 1]}
    while angles_dists_thread.get_angle(POS_O) < 350 and angles_dists_thread.get_angle(POS_O) > 100: ###begins turning to find the houses
        if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
            print("broke in multo")
            break
        global angles_and_dists
        #see if house
        print("seing houses")
        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
        tankDrive.off()
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))

        angle_old = angles_dists_thread.get_angle(POS_O)
        dist_old = angles_dists_thread.ThreadOutput.DIST
        print(dist_old)
        time.sleep(0.07)
        angle_new = angles_dists_thread.get_angle(POS_O)
        dist_new = angles_dists_thread.ThreadOutput.DIST
        print(dist_new)

        if (dist_old - dist_new) < 0 and abs(dist_old - dist_new) >= threshold: ###this is a left edge as the newer distance(to the left of the wall) is longer than the distance to the wall
            print("DIST jump further, left edge")
            #print(dist_old)#debug
            #print(dist_new)#debug
            LEFT_CORNER_ANGLE = angle_old
            LEFT_CORNER_DIST = dist_old + 10
            print(LEFT_CORNER_ANGLE)#debug
            print(LEFT_CORNER_DIST)#debug
            edges[LEFT_CORNER_ANGLE] = [LEFT_CORNER_DIST, 2]
            left_turn(5, 10)
            print("lil turn")

        elif (dist_old - dist_new) > 0 and abs(dist_old - dist_new) >= threshold: ###this is a right adge as the distance gets shorter
            print("DIST jump closer, right edge")
            time.sleep(0.1)
            dist_new = angles_dists_thread.ThreadOutput.DIST
            tankDrive.on(SpeedPercent(0), SpeedPercent(0))
            #print(dist_old)#debug
            #print(dist_new)#debug
            RIGHT_CORNER_ANGLE = angle_new
            RIGHT_CORNER_DIST = dist_new + 10
            print(RIGHT_CORNER_ANGLE)#debug
            print(RIGHT_CORNER_DIST)#debug
            edges[RIGHT_CORNER_ANGLE] = [RIGHT_CORNER_DIST, 1]
            left_turn(5, 10)
            print("lil turn")

        else:
            print("passes")
            if angles_dists_thread.get_angle(POS_O) > 350 or angles_dists_thread.get_angle(POS_O) < 50:
                print("broke in passing")
                break
            continue

    ###sorts the edges according to angle
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)
    leftest_edge = edges[edges_keys[0]]
    if leftest_edge[1] == 2:
        edges[150] = [dist_at_one_o_five, 1] ### if the leftest edge is a left one it sets the value at 150°(the start angle) as the new leftest edge
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)

    for x in range(len(edges)):###determines the angles of approach and the distances to all the houses it finds
        if x % 2 != 0:
            continue
        right = edges[edges_keys[x]]
        left = edges[edges_keys[(x+1)]]
        a = int(right[0])#RIGHT_CORNER_DIST
        b = int(left[0])#LEFT_CORNER_DIST
        alpha = int(edges_keys[x])#RIGHT_CORNER_ANGLE
        beta = int(edges_keys[(x+1)])#LEFT_CORNER_ANGLE
        ANGLE_OF_APPROACH = get_angle_of_appoach(a, b, alpha, beta)
        dist_to_next_house = get_dist_to_next_house(a, alpha, ANGLE_OF_APPROACH)
        angles_and_dists[int(dist_to_next_house)] = int(ANGLE_OF_APPROACH)
        print(left)
        print(right)
        print(alpha)
        print(beta)
        print(angles_and_dists)
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
    to_remove = []
    for x in angles_and_dists.items(): ###goes through all the angles of approach and their corresponding distances and compares them to the actual distance. if the decrepancy is to big it assumes the house its currently looking at is not a valid house to deliver to
        print("checking dists")
        print(x, angles_and_dists[x])
        turn_left_to_x((angles_and_dists[x] + 90), 10)
        print("turning to angle")
        time.sleep(1)
        seen_dist = angles_dists_thread.ThreadOutput.DIST
        if seen_dist > (x-10) + 10 or seen_dist < (x-10) - 10:
            print("doesnt think its right")
            to_remove.append(x)
    for x in to_remove:   ###removes invalid houses
        angles_and_dists.pop(x)
    to_remove.clear()

    time.sleep(0.2)

    print("checked angles and DIST")
