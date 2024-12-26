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

# #import modules.newParallelWallDriveUsingColorCheck
# import modules.test_detect_houses
# import modules.modultwo
# import modules.oldParallelWallDrive

from modules.anglesDistsThread import *
import modules.parallelWallDrive
import modules.detectHousesPrimitive
import modules.turning

studmm = 7
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)
#or: moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
#colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
#ultraSoundSensor = UltrasonicSensor(INPUT_3)

stop_event = threading.Event()

col_raw = [0, 0, 0]
tbdDistance = 10
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

time.sleep(0.3)

def main():
    
    print("please press")
    #play tone
    global seesRed
    global seesGreen

    startThreads()
    global zero
    zero = threadOutput.circleAngle

    Sound().play_file('/home/robot/ev3/miscellaneous/soundFiles/Audio1.wav', volume=100, play_type=0)
    
    while True:
        if Button().any() == True:
           break
        time.sleep(0.05)
    global posO
    posO = threadOutput.circleAngle
    zero = 90
    

    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
    time.sleep(0.5)
    #figure out how to detect an adge and drive parallel to a wall and see red
    color = [False, False, False]
    while True:
        color = modules.parallelWallDrive.main()
        if color[1] == True:
            print("red")
            tankDrive.off()   
            seesRed = False

            posO = threadOutput.circleAngle
            
            #getMultipleHouses()
            modules.detectHousesPrimitive.getHousePrimitive()

            #debug_WARNING: I am very unsure if this will work, please make sure it doesn't give an error
            wantedAnOfAprch = int(float(modules.detectHousesPrimitive.anglesAndDists[modules.detectHousesPrimitive.dist_short]))
            
            #debug_WARNING: does the new file (test_detect_houses) already do this, or does it need to be done here?
            modules.turning.turntoxr(50, 10)
            drop()
            time.sleep(0.5)
            print("checking dists")
            modules.turning.turntoxl((wantedAnOfAprch + 90), 10)
            print("turning to angle")
            time.sleep(0.5)
            seenDist = threadOutput.dist
            print(seenDist)
            time.sleep(0.2)
            modules.turning.turntoxr(wantedAnOfAprch, 10)


            toDriveDist = seenDist - 13
            if toDriveDist > 5:
                driveTillDistWheel(toDriveDist)
                print("drove")
            
            #moveDifferential.turn_left(10, 90)
            modules.turning.relturnv(90, 10)
            #leftTurn(90, 10)
            time.sleep(0.2)
            seesRed = False
            #tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.5)
            posO = threadOutput.circleAngle

            #then drive to thew next house and then turn  
        
        if color[2] == True: 
            tankDrive.off()
            seesGreen = False
            print("green")
            smoothDriveStraight(20)
            time.sleep(3)
            tankDrive.off()
            break
        #drive parallel to wall
        #adjustDist_findEdge(17, 4, 10, 20, (0.9*22.3))
        #modules.newParallelWallDriveUsingColorCheck.main()'''


'''def readColor():
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
        time.sleep(0.1)'''
    
def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.75)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.75)


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
# def betterTurnRightToX(degrees, speed):
#     moveDifferential.odometry_start()
#     moveDifferential.turn_to_angle(SpeedPercent(speed), degrees)
#     moveDifferential.odometry_stop()

# def betterTurnLeftToX(degrees, speed):
#     moveDifferential.odometry_start()
#     moveDifferential.turn_to_angle(SpeedPercent(-speed), degrees)
#     moveDifferential.odometry_stop()

# def leftTurn(degrees, speed):
#     angle = getAngle()
#     startAngle = angle
#     while angle < min(350,(startAngle + degrees)):
#         tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
#         angle = getAngle()
#         if angle > 350:
#             break
#     tankDrive.on(SpeedPercent(0), SpeedPercent(0))

# #moveDifferential.turn_left(SpeedPercent(speed), degrees)

# def rightTurn(degrees, speed):
#     angle = getAngle()
#     startAngle = angle
#     while angle > max((startAngle - degrees), 10):
#         tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
#         angle = getAngle()
#         if angle < 10:#if it slightly overturns at a 90°turn from ninety degrees
#             break
#     tankDrive.on(SpeedPercent(0), SpeedPercent(0))

# #moveDifferential.turn_right(SpeedPercent(speed), degrees)

# def turnRightToX(degrees, speed):
#     angle = getAngle()
#     while angle > max(10, degrees - 5):
#         #moveDifferential.turn_right(speed, 1)
#         tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
#         angle = getAngle()
#     tankDrive.on(SpeedPercent(0), SpeedPercent(0))

# def turnLeftToX(degrees, speed):
#     angle = getAngle()
#     while angle < min(degrees + 5, 350):
#         tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
#         #moveDifferential.turn_left(speed, 1)
#         angle = getAngle()
#     tankDrive.on(SpeedPercent(0), SpeedPercent(0))

#determine how to get to next house
# def detectHouseEdges(threshold):
#     #betterTurnRightToX(7, 7)
#     print("seeking")
#     global rightCornerAngle
#     global leftCornerAngle
#     global rightCornerDist
#     global leftCornerDist
#     tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
#     while True:
#         if getAngle() > 350 or getAngle() < 50:
#             tankDrive.off()
#             break
#         angleOld = getAngle()
#         distOld = dist
#         print(distOld)
#         time.sleep(0.07)
#         angleNew = getAngle()
#         distNew = dist
#         print(distNew)
#         if distNew > 0:
#             if abs(distOld-distNew) >= threshold:
#                 time.sleep(0.1)
#                 distNew = dist
#                 tankDrive.on(SpeedPercent(0), SpeedPercent(0))
#                 rightCornerAngle = angleNew
#                 rightCornerDist = distNew + 10
#                 print(rightCornerAngle)#debug
#                 print(rightCornerDist)#debug
#                 break
#     print("found one")#debug
#     tankDrive.off()
#     time.sleep(1)
#     #betterTurnDegrees(5, 15)
#     if getAngle() < 350 and getAngle() > 150:
#         #moveDifferential.turn_left(10, 5)
#         leftTurn(5, 10)
#         print("lil turn")
#         tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
        
#     while True:
#         if getAngle() > 350 or getAngle() < 50:
#             break
#         #this here so it doesnt get stuck indefinitly executing
#         angleOld = getAngle()
#         distOld = dist
#         print(distOld)
#         time.sleep(0.07)
#         angleNew = getAngle()
#         distNew = dist
#         print(distNew)
#         if abs(distOld-distNew) >= threshold:
#             leftCornerAngle = angleOld
#             leftCornerDist = distOld + 10
#             print(leftCornerAngle)#debug
#             print(leftCornerDist)#debug
#             break
#     tankDrive.off()
#     print("right Corner Angle: " + str(rightCornerAngle)  + ", right Corner distance: " + str(rightCornerDist)) #debug
#     print("left Corner Angle: " + str(leftCornerAngle)+ ", left Corner distance: " + str(leftCornerDist)) #debug

# def getMultipleHouses():
    
#     #drive forward about 1x the length of the robot from the sensor to the turning radius (~16cm)
#     tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 0.718)
#     tankDrive.off()
#     print(getAngle())
#     tankDrive.off()
#     time.sleep(0.5)
#     global posO
#     posO = circleAngle
#     time.sleep(0.5)
#     print(getAngle())
#     time.sleep(0.5)
#     print("driven")
#     turnLeftToX(150, 10) #turn so that the sensor points outwards
#     print("turned outwards")
#     time.sleep(0.5)
#     while getAngle() < 350 and getAngle() > 100:
#         if getAngle() > 350 or getAngle() < 50:
#             print("broke in multo")
#             break
#         global anglesAndDists
#         #see if house
#         print("seing houses")
#         detectHouseEdges(12)
#         tankDrive.on(SpeedPercent(0), SpeedPercent(0))
#         tankDrive.off()
#         print("saw houses")
        
#         a = rightCornerDist 
#         b = leftCornerDist 
#         alpha = rightCornerAngle
#         beta = leftCornerAngle

#         anOfAprch = getAngleOfApproach(a, b, alpha, beta)

#         distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)

#         anglesAndDists[int(distToNextHouse)] = int(anOfAprch)

#         if getAngle() > 350 or getAngle() < 50:
#             print("broke in multo2")
#             break

#         time.sleep(1)
#         #moveDifferential.turn_left(5, 10)
#         leftTurn(5, 10)

#     print("checked for houses")

#     tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
#     time.sleep(5)
#     tankDrive.off()

#     turnRightToX(150, 10)
#     print("turned back")
#     time.sleep(1)

#     print("checked angles and dist")
        
# def getAngleOfApproach(a, b, alpha, beta):
#     global anOfAprch
#     try:
#         anOfAprch = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
#     except ZeroDivisionError:
#         anOfAprch = 90
#         print("Angle of Approach calculation: zero division error")
#     except:
#         print("Angle of Approach calculation: unknown error")
#     return anOfAprch

# def getDistToNextHouse(a, alpha, anOfAprch):
#     distToNextHouse = abs(math.cos(anOfAprch - alpha)) * a
#     return distToNextHouse

if __name__=="__main__":
    main()