"""module containing functions for turning"""
#!/usr/bin/env python3

import time

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
import modules.anglesDistsThread #imports needed values from the thread moudule

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

def turn_right_to_x(degrees, speed):
    """function turning to a specific angle in a specific direction"""
    cpos = modules.anglesDistsThread.modules.anglesDistsThread.threadOutput.circleAngle
    if (degrees>cpos):          ###
        langle = cpos+360       ### this part ensures that the robot can turn to angles to the left of the current angle
    else:                       ###
        langle=cpos             ###
    tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
    while langle > (degrees + 5):
        if (modules.anglesDistsThread.threadOutput.circleAngle<=cpos):       ### this part ensures that the robot can turn to angles to the left of the current angle
            langle = modules.anglesDistsThread.threadOutput.circleAngle+360  ###
        else:                                      ###
            langle = modules.anglesDistsThread.threadOutput.circleAngle      ###
        print("right:  "+ langle)
    tank_drive.off()

def turn_left_to_x(degrees, speed):
    cpos = modules.anglesDistsThread.threadOutput.circleAngle 
    if (degrees<cpos):      ###
        langle = cpos-360   ### this part ensures that the robot can turn to angles to the right of the current angle
    else:                   ###
        langle=cpos         ###
    tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed)) 
    while langle < (degrees - 5):       
        if (modules.anglesDistsThread.threadOutput.circleAngle>=cpos):        ### this part ensures that the robot can turn to angles to the right of the current angle
            langle = modules.anglesDistsThread.threadOutput.circleAngle-360   ###
        else:                                       ###
            langle = modules.anglesDistsThread.threadOutput.circleAngle       ###
        print("left:  "+ langle)
    tank_drive.off()


#function to turn for a specific amount of degrees in a direction specified when calling the function
def relative_turn(degrees, speed):
    cpos = modules.anglesDistsThread.threadOutput.Angle  
    while abs(modules.anglesDistsThread.getRelAngle(cpos)) < max(degrees, 10): # min turn: 10°
        tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
    tank_drive.off()
# turning functions using relative_turn
def leftTurn(degrees, speed):
    relative_turn(degrees,-speed)
def rightTurn(degrees, speed):
    relative_turn(degrees, speed)

#funtions to turn to a specific angle (left or right turns) with a tolerance
def turn_to_x_left(degrees, speed):
    cpos = modules.anglesDistsThread.threadOutput.circleAngle
    target = degrees
    tolerance=5                                                     ### the if else statements ensure that it can also turn to angles which are to the right of the current angle
    if (target>=cpos):
        while modules.anglesDistsThread.threadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        npos=360
        while ((modules.anglesDistsThread.threadOutput.circleAngle-npos<target-tolerance)):
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if cpos-modules.anglesDistsThread.threadOutput.circleAngle>0:
                npos=0
    tank_drive.off()

def turn_to_x_right(degrees, speed):
    cpos = modules.anglesDistsThread.threadOutput.circleAngle
    target = degrees
    tolerance=5                                                     ### the if else statements ensure that it can also turn to angles which are to the left of the current angle
    if (target<cpos):
        while modules.anglesDistsThread.threadOutput.circleAngle > target+tolerance:
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
    else:
        npos=360
        while ((modules.anglesDistsThread.threadOutput.circleAngle+npos>target+tolerance)):
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            if cpos-modules.anglesDistsThread.threadOutput.circleAngle<0:
                npos=0
    tank_drive.off()

# an attempt to also use tolerances in a turning functions for a relative turn of x° not a turn to x° (in this case a left turn)
def relative_turnv(degrees, speed):
    cpos = modules.anglesDistsThread.threadOutput.circleAngle
    target = cpos + degrees
    tolerance=5
    if target<360:                                                  ### the if else statements ensure that it can also turn to angles which are to the right of the current angle
        while modules.anglesDistsThread.threadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        npos=0
        while (modules.anglesDistsThread.threadOutput.circleAngle+npos<target-tolerance):
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if modules.anglesDistsThread.threadOutput.circleAngle<cpos:
                npos=360
    tank_drive.off()