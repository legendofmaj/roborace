#!/usr/bin/env python3
"""module to drive parallel to a wall and get the current color"""

import math
import time

#import the necessary libraries
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, SpeedPercent, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

import turning
import angles_dists_thread

#create the sensors and motors objects
motorA = LargeMotor(OUTPUT_C)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_C, OUTPUT_B)
color_sensor = ColorSensor(INPUT_1)

dist_arrayx = (list(range(0,360)))
dist_array = (list(range(0,360)))
MINIMUM_DIST = 1000000
MINIMUM_PHI = 1000000
MINIMUM_DIST_AVERAGE = 1000000
MINIMUM_PHI_AVERAGE = 1000000

def main():
    """function to calculate turnratio using pid-algorithm"""
    #values for pid tuning
    kp = 1.0
    ki = 0.2
    kd = 0.2

    #other values for tuning
    goal = 13#cm

    #define other important values
    integral = 0
    previous_error = 0
    delta_time = 0
    stopint = 1
    countd = 0 #used for handeling extreme turn rations to prevent the robot from completly overturning
    countv = 0
    previous_time = time.time()
    time.sleep(0.01) #a quick break, to not get a zero division error

    while True:
        current_time = time.time()
        delta_time = current_time - previous_time

        error = angles_dists_thread.ThreadOutput.dist - goal
        integral += stopint*(error * delta_time)
        derivative = (error - previous_error) / delta_time

        #correction of unsafe pid values
        if abs(error) > 10.0:
            kp = 0.2
        else:
            kp = 1.0
        if abs(derivative) > 100:
            kd = 1.0
            ki = 0.02
            stopint = 0
            countd += 1
        elif 0 < countd < 4:
            countd += 1
        else:
            kd = 0.2
            ki = 0.2
            stopint = 1
            countd = 0

        #calculate turnratio with pid-algorithm
        turnratio = (kp * error) + (ki * integral) + (kd * derivative)
        turnratio_calculated = turnratio

        #limit turnratio to safe values
        if turnratio > 25:
            turnratio = 25
            if (error - previous_error) > 0:
                countv += 1
        elif turnratio < -100:
            turnratio = -100
        #if the turn ratio gets too high / low the robot will turn too aggressivly, this is supposed to prevent that
        if countv > 20:
            turnratio = 0
            for i in dist_arrayx:
                dist_array[i]= 20+15.0*(1-(math.sin(i*math.pi/360)*math.sin(i*math.pi/360)))

            swipelr()
            print("------------ mind Avg:",MINIMUM_DIST_AVERAGE)
            print("------------ minphi Avg:",MINIMUM_PHI_AVERAGE)

            print("turning left absolut")

            turning.turn_to_x_left(MINIMUM_PHI_AVERAGE,10.0)
            time.sleep(1)
            countv=0

        print("distance: " + str(angles_dists_thread.ThreadOutput.dist))
        print("error: " + str(error))
        print("turnratio calculated: " + str(turnratio_calculated))
        print("turnratio limited: " + str(turnratio))
        print("countv: " + str(countv)+ " countd: " + str(countd))
        print("delta_time: " + str(delta_time) + "    deriv: " + str(derivative))

        #plug value calculated by pid-algorithm into steering function
        steering_drive.on(turnratio, -20)

        previous_error = error
        previous_time = current_time

        #check color while steering (used in main file)
        checked_color = check_color()
        if checked_color[0] is True:
            return checked_color


def check_color():
    """function to check the current color"""
    color_seen = [
        False,
        False,
        False
    ]
    raw_color = color_sensor.color
    col_raw = color_sensor.raw
    if raw_color == 5:
        color_seen[1] = True
        color_seen[0] = True
        color_seen[2] = False
    elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
        color_seen[0] = True
        color_seen[2] = True
        color_seen[1] = False
    return color_seen

def swipelr():
    """function to rotate the robot left and right"""
    global MINIMUM_DIST_AVERAGE
    global MINIMUM_PHI_AVERAGE
    print("swiping left")

    relative_swipe_right(90, 10.0)

    time.sleep(1)

    left_minimum_dist = MINIMUM_DIST
    left_phi = MINIMUM_PHI

    print("swiping right")

    relative_swipe_left(120, 10.0)
    time.sleep(1)
    MINIMUM_DIST_AVERAGE = (MINIMUM_DIST+left_minimum_dist)/2
    MINIMUM_PHI_AVERAGE = (MINIMUM_PHI+left_phi)/2
    print("mind l:",left_minimum_dist,"mind r:",MINIMUM_DIST,"mind Avg:",MINIMUM_DIST_AVERAGE)
    print("minphi l:",left_phi,"mind r:",MINIMUM_PHI,"mind Avg:",MINIMUM_PHI_AVERAGE)

    turning.turn_to_x_right(MINIMUM_PHI_AVERAGE, 10) #turn_to_x_right

def relative_swipe_left(degrees, speed):
    """function to swipe / rotate left, relative to the current position to realign to the wall at sharp corners"""
    global MINIMUM_DIST
    global MINIMUM_PHI
    current_pos = angles_dists_thread.ThreadOutput.circleAngle
    target = current_pos + degrees
    print("relturnv.target:",target)
    tolerance = 5
    if target < 360:
        while angles_dists_thread.ThreadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            print("relturnv.circleAngle1:", angles_dists_thread.ThreadOutput.circleAngle)
            dist_phi = dist_array[int(angles_dists_thread.ThreadOutput.circleAngle)]
            print("distance:",dist_phi)
            if dist_phi < MINIMUM_DIST:
                MINIMUM_DIST = dist_phi
                MINIMUM_PHI = angles_dists_thread.ThreadOutput.circleAngle
        print("relturnv.Done1")
    else:
        null_pos = 0
        while angles_dists_thread.ThreadOutput.circleAngle + null_pos < target - tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if angles_dists_thread.ThreadOutput.circleAngle < current_pos:
                null_pos = 360
            print("relturnv.circleAngle2:", angles_dists_thread.ThreadOutput.circleAngle)
            dist_phi = dist_array[int(angles_dists_thread.ThreadOutput.circleAngle)]
            print("distance:",dist_phi)
            if dist_phi < MINIMUM_DIST:
                MINIMUM_DIST = dist_phi
                MINIMUM_PHI = angles_dists_thread.ThreadOutput.circleAngle
        print("relturnv.Done2")
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnv.Done3")
    print("minphi:",MINIMUM_PHI,"mind:",MINIMUM_DIST)

def relative_swipe_right(degrees, speed):
    """function to swipe / rotate right, relative to the current position"""
    global MINIMUM_DIST
    global MINIMUM_PHI

    current_pos = angles_dists_thread.ThreadOutput.circleAngle
    target = current_pos - degrees
    print("relative_swipe_right.target:",target)
    tolerance = 5
    if target > 0:
        while angles_dists_thread.ThreadOutput.circleAngle > target+tolerance:
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            print("relative_swipe_right.circleAngle1: ", end="")
            print(angles_dists_thread.ThreadOutput.circleAngle)
            dist_phi = dist_array[int(angles_dists_thread.ThreadOutput.circleAngle)]
            print("relative_swipe_right.distance1:",dist_phi)
            if dist_phi < MINIMUM_DIST:
                MINIMUM_DIST = dist_phi
                MINIMUM_PHI = angles_dists_thread.ThreadOutput.circleAngle
        print("relative_swipe_right.Done1")
    else:
        null_pos = 0
        while ((angles_dists_thread.ThreadOutput.circleAngle-null_pos>target+tolerance)):
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            if current_pos - angles_dists_thread.ThreadOutput.circleAngle < 0:
                null_pos = 360
            print("relative_swipe_right.circleAngle2:", end="")
            print(angles_dists_thread.ThreadOutput.circleAngle)
            dist_phi = dist_array[int(angles_dists_thread.ThreadOutput.circleAngle)]
            print("relative_swipe_right.distance2:",dist_phi)
            if dist_phi < MINIMUM_DIST:
                MINIMUM_DIST = dist_phi
                MINIMUM_PHI = angles_dists_thread.ThreadOutput.circleAngle
        print("relative_swipe_right.Done2")
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    print("relative_swipe_right.Done3")
    print("minphi:",MINIMUM_PHI,"mind:",MINIMUM_DIST)
# End-of-file (EOF)
