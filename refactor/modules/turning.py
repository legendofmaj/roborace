#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire

from modules.anglesDistsThread import *

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)

def turnRightToX(degrees, speed):
    cpos = threadOutput.circleAngle
    if (degrees>cpos):
        langle = cpos+360
    else:
        langle=cpos
    tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
    while langle > (degrees + 5):
        if (threadOutput.circleAngle<=cpos):
            langle = threadOutput.circleAngle+360
        else:
            langle = threadOutput.circleAngle
        print("right:  "+ langle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    cpos = threadOutput.circleAngle 
    if (degrees<cpos):
        langle = cpos-360
    else:
        langle=cpos
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed)) 
    while langle < (degrees - 5):
        if (threadOutput.circleAngle>=cpos):
            langle = threadOutput.circleAngle-360
        else:
            langle = threadOutput.circleAngle
        print("left:  "+ langle)
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    relturn(degrees, speed)

def relturn(degrees, speed):
    cpos = threadOutput.Angle
    startAngle = getRelAngle(cpos)
    while abs(getRelAngle(cpos)) > max(degrees, 10):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def leftTurn(degrees, speed):
    relturn(degrees,-speed)


def turntoxl(degrees, speed):
    cpos = threadOutput.circleAngle
    target = degrees
    tolerance=5
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
    tolerance=5
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

# turning left
def relturnv(degrees, speed):
    cpos = threadOutput.circleAngle
    target = cpos + degrees
    tolerance=5
    if target<360:
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