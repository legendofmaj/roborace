#!/usr/bin/env python3

#contains functions for turning

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire

from modules.anglesDistsThread import * #imports needed values from the thread moudule

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)


#turns to a specific angle in a specific direction
def turnRightToX(degrees, speed):
    cpos = threadOutput.circleAngle
    if (degrees>cpos):          ###
        langle = cpos+360       ### this part ensures that the robot can turn to angles to the left of the current angle
    else:                       ###
        langle=cpos             ###
    tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
    while langle > (degrees + 5):
        if (threadOutput.circleAngle<=cpos):       ### this part ensures that the robot can turn to angles to the left of the current angle
            langle = threadOutput.circleAngle+360  ###
        else:                                      ###
            langle = threadOutput.circleAngle      ###
        print("right:  "+ langle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    cpos = threadOutput.circleAngle 
    if (degrees<cpos):      ###
        langle = cpos-360   ### this part ensures that the robot can turn to angles to the right of the current angle
    else:                   ###
        langle=cpos         ###
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed)) 
    while langle < (degrees - 5):       
        if (threadOutput.circleAngle>=cpos):        ### this part ensures that the robot can turn to angles to the right of the current angle
            langle = threadOutput.circleAngle-360   ###
        else:                                       ###
            langle = threadOutput.circleAngle       ###
        print("left:  "+ langle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))


#function to turn for a specific amount of degrees in a direction specified when calling the function
def relturn(degrees, speed):
    cpos = threadOutput.Angle  
    while abs(getRelAngle(cpos)) < max(degrees, 10): # min turn: 10°
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
# turning functions using relturn
def leftTurn(degrees, speed):
    relturn(degrees,-speed)
def rightTurn(degrees, speed):
    relturn(degrees, speed)

#funtions to turn to a specific angle (left or right turns) with a tolerance
def turntoxl(degrees, speed):
    cpos = threadOutput.circleAngle
    target = degrees
    tolerance=5                                                     ### the if else statements ensure that it can also turn to angles which are to the right of the current angle
    if (target>=cpos):
        while threadOutput.circleAngle < target-tolerance:
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        npos=360
        while ((threadOutput.circleAngle-npos<target-tolerance)):
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if cpos-threadOutput.circleAngle>0:
                npos=0
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turntoxr(degrees, speed):
    cpos = threadOutput.circleAngle
    target = degrees
    tolerance=5                                                     ### the if else statements ensure that it can also turn to angles which are to the left of the current angle
    if (target<cpos):
        while threadOutput.circleAngle > target+tolerance:
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
    else:
        npos=360
        while ((threadOutput.circleAngle+npos>target+tolerance)):
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            if cpos-threadOutput.circleAngle<0:
                npos=0
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

# an attempt to also use tolerances in a turning functions for a relative turn of x° not a turn to x° (in this case a left turn)
def relturnv(degrees, speed):
    cpos = threadOutput.circleAngle
    target = cpos + degrees
    tolerance=5
    if target<360:                                                  ### the if else statements ensure that it can also turn to angles which are to the right of the current angle
        while threadOutput.circleAngle < target-tolerance:
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
    else:
        npos=0
        while (threadOutput.circleAngle+npos<target-tolerance):
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if threadOutput.circleAngle<cpos:
                npos=360
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))