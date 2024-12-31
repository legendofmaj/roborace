"""module containing functions for turning"""
#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
import modules.anglesDistsThread #imports needed values from the thread moudule

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

def turn_right_to_x(degrees, speed):
    """function turning to a specific angle in a specific direction"""
    current_pos = modules.anglesDistsThread.modules.anglesDistsThread.threadOutput.circleAngle
    #this part ensures that the robot can turn to angles to the left of the current angle
    if degrees > current_pos:
        left_angle = current_pos + 360
    else:
        left_angle=current_pos
    tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
    while left_angle > (degrees + 5):
        #this part ensures that the robot can turn to angles to the left of the current angle
        if modules.anglesDistsThread.threadOutput.circleAngle <= current_pos:
            left_angle = modules.anglesDistsThread.threadOutput.circleAngle + 360
        else:
            left_angle = modules.anglesDistsThread.threadOutput.circleAngle
        print("right:  " + left_angle)
    tank_drive.off()

def turn_left_to_x(degrees, speed):
    """function that turns left to specified number of degrees"""
    current_pos = modules.anglesDistsThread.threadOutput.circleAngle
    #this part ensures that the robot can turn to angles to the right of the current angle
    if degrees < current_pos:
        left_angle = current_pos - 360
    else:
        left_angle=current_pos
    tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
    while left_angle < (degrees - 5):
        #this part ensures that the robot can turn to angles to the right of the current angle
        if modules.anglesDistsThread.threadOutput.circleAngle >= current_pos:
            left_angle = modules.anglesDistsThread.threadOutput.circleAngle - 360
        else:
            left_angle = modules.anglesDistsThread.threadOutput.circleAngle
        print("left:  " + left_angle)
    tank_drive.off()


def relative_turn(degrees, speed):
    """function to turn for a specific amount of degrees in a direction specified"""
    current_pos = modules.anglesDistsThread.threadOutput.Angle
    while abs(modules.anglesDistsThread.getReleft_angle(current_pos)) < max(degrees, 10):
        #min turn: 10°
        tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
    tank_drive.off()

def left_turn(degrees, speed):
    """turning functions using relative_turn"""
    relative_turn(degrees,-speed)

def turn_right(degrees, speed):
    """turning functions using relative_turn"""
    relative_turn(degrees, speed)

def turn_to_x_left(degrees, speed):
    """funtion to turn to a specific angle (left) with a tolerance"""
    current_pos = modules.anglesDistsThread.threadOutput.circleAngle
    target = degrees
    tolerance = 5
    #the if else statements ensure that it can also turn to angles
    #which are to the right of the current angle
    if target >= current_pos:
        while modules.anglesDistsThread.threadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        null_pos = 360
        while modules.anglesDistsThread.threadOutput.circleAngle-null_pos<target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if current_pos - modules.anglesDistsThread.threadOutput.circleAngle > 0:
                null_pos=0
    tank_drive.off()

def turn_to_x_right(degrees, speed):
    """function to turn to a specific angle (right) with a tolerance"""
    current_pos = modules.anglesDistsThread.threadOutput.circleAngle
    target = degrees
    tolerance = 5
    #the if else statements ensure that it can also turn to angles
    #which are to the left of the current angle
    if target < current_pos:
        while modules.anglesDistsThread.threadOutput.circleAngle > target + tolerance:
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
    else:
        null_pos = 360
        while modules.anglesDistsThread.threadOutput.circleAngle+null_pos > target + tolerance:
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            if current_pos - modules.anglesDistsThread.threadOutput.circleAngle < 0:
                null_pos = 0
    tank_drive.off()

def relative_turnv(degrees, speed):
    """an attempt to also use tolerances in a turning functions for a relative turn of x°
    not a turn to x° (in this case a left turn)"""
    current_pos = modules.anglesDistsThread.threadOutput.circleAngle
    target = current_pos + degrees
    tolerance = 5
    if target < 360:
        #the if else statements ensure that it can also turn to angles which
        #are to the right of the current angle
        while modules.anglesDistsThread.threadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        null_pos = 0
        while modules.anglesDistsThread.threadOutput.circleAngle + null_pos < target - tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if modules.anglesDistsThread.threadOutput.circleAngle < current_pos:
                null_pos = 360
    tank_drive.off()
# End-of-file (EOF)
