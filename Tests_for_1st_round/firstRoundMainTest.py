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




studmm = 8
studs_that_wheels_are_apart = 15
min_dist_between_wheels = 118 #mm
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, studs_that_wheels_are_apart * studmm)
#or: mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, min_dist_between_wheels)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
#tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
speaker = Sound()
#tankDrive.gyro = gyroSensor

stop_event = threading.Event()

col_raw = [0, 0, 0]
tbdDistance = 10
dist = 0.0
circleAngle = 90
rightCornerDist = 0.0
leftCornerDist = 0.0
rightCornerAngle = 0
leftCornerAngle = 0
anOfAprch = 0.0
seesGreen = False
seesRed = False

anglesAndDists = {1000000 : 1000000}

posO = 90
Angle = 90

#gyroSensor.reset()
#tankDrive.gyro.reset()
time.sleep(1)

def main():
    print("u may press")
    #play tone
    global seesRed
    global seesGreen

    #gyroSensor.reset()

    startThreads()

    #startingFanfare()
    
    #while True:
    #    if buttonPressed == True:
    #        break
    #    time.sleep(0.05)

    #tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
    time.sleep(2)
    #figure out how to detect an adge and drive parallel to a wall and see red
    while True:
        if seesRed == True:
            print("red")
            tankDrive.off()   
            seesRed = False
            #gyroSensor.reset()
            
            getMultipleHouses()

            #add the dists to a list and sort it
            distsToNextHouse = anglesAndDists.keys()
            print(distsToNextHouse, anglesAndDists.keys())
            distsToNextHouse = [float(x) for x in distsToNextHouse]
            distsToNextHouse = sorted(distsToNextHouse)
            print(distsToNextHouse)
            #figure out which one is the shortest and save it, also figure out which is the correspaonding angle and save it
            shortestDist = float(distsToNextHouse[0])
            wantedAnOfAprch = int(float(anglesAndDists[shortestDist]))

            #drop abd 
            turnRightToX(50, 10)
            drop()
            time.sleep(0.5)

            turnLeftToX(wantedAnOfAprch, 10)

            toDriveDist = shortestDist - 20
            if toDriveDist > 5:
                driveTillDistWheel(toDriveDist)
            
            leftTurn(90, 10)

            #then drive to thew next house and then turn  
        
        if seesGreen == True: 
            tankDrive.off()
            seesGreen = False
            print("green")
            smoothDriveStraight(20)
            time.sleep(3)
            tankDrive.off()
            break
        
        adjustDist_findEdge(11, 4, 10, 35, (0.9*22.3))

    #finishFanfare()

def startThreads():
    distThread = threading.Thread(target= read_dist)
    distThread.start()
    buttonThread = threading.Thread(target = readButton)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target = readColor)
    colorThread.start()
    #angleThread = threading.Thread(target = readAngle)
    #angleThread.start()
    circleAngleThread = threading.Thread(target = readCircleAngle)#, args=(stop_event))
    circleAngleThread.start()

def startingFanfare():
    speaker.play_song([('C4',500), ('F4',250), ('C4',250)])#to be played before starting to navigate thru course

def finishFanfare():
    speaker.play_song([('C4', 400), ('E4', 400), ('G4', 400), ('B4', 400), ('G4', 400), ('B4', 650)])#to be played after finishing course


def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

def readButton():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break
    print("started") #debug

def readColor():
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
        #elif rawColor == 3:
        #    color = "green"
        elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            color = "green"
            seesGreen = True
        time.sleep(0.1)

def readAngle():
    #global angle
    while True:
     #   angle = gyroSensor.angle
        time.sleep(0.05)

def readCircleAngle():
    global circleAngle
    while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)

def getAngle():
    global posO
    #global Angle
    temp = (circleAngle - posO) + 90
    if temp < 0:
        return temp + 360
    elif temp > 360:
        return temp - 360
    else:
        return temp

    
def drop():
    print("dropping") #debug
    depositMotor.on_for_rotations(SpeedPercent(75), 1.9)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.9)

'''def detectJumpInDist(threshold, dist):
    while True:
        distOld = ultraSoundSensor.distance_centimeters
        time.sleep(0.005)
        distNew = ultraSoundSensor.distance_centimeters
        if distOld < 50:
            if abs(distOld-distNew) >= threshold:
                print("sees edge")
                rotations = 0.00
                while True:
                    tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), 0.01)
                    rotations += 0.01
                    dist_crossed = rotations* 22.3 #in cm
                    if dist_crossed >= dist:
                        tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                        #circleAngle = gyroSensor.circle_angle()
                        break
                tankDrive.turn_degrees(SpeedPercent(5), -90)'''

def adjustDist_findEdge(desired_dist, tolerance, speed, threshold, drive_further):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    #print("jeah no")
    #global distOld
    #threshold, drive_further = 35, 22.3
    correct = 0
    if dist > desired_dist  + tolerance:
        print("dist too big")
        correct = 1
    elif dist < desired_dist - tolerance:
        print("dist too small")
        correct = -1
    elif dist > desired_dist - tolerance and dist < desired_dist + tolerance:
        correct = 0
        print("hmm sees to be right")
    tankDrive.off()
    if correct == 1: #it starts turning outwards for some rteason and doesnt turn abcjk in
        distOld = dist
        rightTurn(4, 10)
        #tankDrive.off()
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.1) 
        #distOld = dist
        #time.sleep(0.5)
        #tankDrive.off()
        leftTurn(4, 10)
        #tankDrive.off() 
        distNew = dist
    if correct == -1:
        distOld = dist
        leftTurn(4, 10)
        tankDrive.off()
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.1)
        #distOld = dist
        #time.sleep(0.5)
        tankDrive.off()
        #print("gets herd")
        rightTurn(3, 10)
        tankDrive.off()
        distNew = dist
        #print("hello is past second turn")
    if correct == 0:
        distOld = dist
        tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), 0.1)
        distNew = dist
        #time.sleep(0.3)
    if distOld < 50:
        if abs(distOld-distNew) >= threshold: # this works best when it dosnt need to turn first otherwise might seen an edge where ther isnt one
            print("sees edge")
            rotations = 0.00
            while True:
                rotation = 0.9
                tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), rotation)
                rotations += rotation
                dist_crossed = rotations* 22.3 #in cm
                if dist_crossed >= drive_further:
                    tankDrive.off()
                    break

            rightTurn(85, 10) #should be ninety overturns tho
            tankDrive.off()
            time.sleep(1)
            tankDrive.on(SpeedPercent(0), SpeedPercent(0))
            time.sleep(0.1)
            tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1.5) #this works very inconsistently
            time.sleep(2)
            print(getAngle())
            tankDrive.off()
            time.sleep(1.5)
            #gyroSensor.reset()
            global posO
            posO = circleAngle
            print(getAngle())
            time.sleep(1)

#driving
def driveStraight(speed, rotations):
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smoothDriveStraight(speed):
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def driveTillDist(distance): #this doesnt work anymore
    while True:
        if dist <= distance:
            print("broke") #debug
            break
        driveStraight(20, 0.1)
        print("rolled") #debug

def driveTillDistWheel(dist):
    #tankDrive.on(SpeedPercent(-5), SpeedPercent(-5))
    rotations = 0.00
    while True:
        tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), 0.03)
        rotations += 0.03
        dist_crossed = rotations * 22.3 #in cm
        if dist_crossed >= dist:
            break

#turning
def betterTurnDegrees(degrees, speed):
    mdiff.odometry_start()
    mdiff.turn_to_angle(SpeedPercent(speed), degrees)
    mdiff.odometry_stop()
def leftTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle <= (startAngle + degrees):
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def rightTurn(degrees, speed):
    angle = getAngle()
    startAngle = angle
    while angle >= max((startAngle - degrees), 0):
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
        if angle > 350 and angle <= 360:#if it slightly overturns at a 90°turn from ninety degrees
            break
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnRightToX(degrees, speed):
    angle = getAngle()
    while angle > degrees:
        tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

def turnLeftToX(degrees, speed):
    angle = getAngle()
    while angle < degrees:
        tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
        angle = getAngle()
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))

#determine how to get to next house
def detectHouseEdges(threshold):
    #gyroSensor.reset()
    #turnRightToX(7, 7)
    print("seeking")
    global rightCornerAngle
    global leftCornerAngle
    global rightCornerDist
    global leftCornerDist
    tankDrive.on(SpeedPercent(-5), SpeedPercent(5))
    while True:
        if getAngle() > 350 or getAngle() < 50:
            tankDrive.off()
            print("nope")
            break
        angleOld = getAngle()
        distOld = dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = dist
        print(distNew)
        if distNew > 0:
            if abs(distOld-distNew) >= threshold:
                tankDrive.on(SpeedPercent(0), SpeedPercent(0))
                #print(distOld)#debug
                #print(distNew)#debug
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
        leftTurn(5, 10)
        print("lil turn")
        tankDrive.on(SpeedPercent(-3), SpeedPercent(3))
        
    while True:
        if getAngle() > 350 or getAngle() < 50:
            print("broke")
            break
        #this here so it doesnt get stuck indefinitly executing
        angleOld = getAngle()
        distOld = dist
        print(distOld)
        time.sleep(0.07)
        angleNew = getAngle()
        distNew = dist
        print(distNew)
        if abs(distOld-distNew) >= threshold:
            #print(distOld)#debug
            #print(distNew)#debug
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
    time.sleep(1.5)
    #gyroSensor.reset()
    global posO
    posO = circleAngle
    time.sleep(0.5)
    print(getAngle())
    time.sleep(0.5)
    print("driven")
    turnLeftToX(180, 10) #turn so that the sensor points outwards
    print("turned outwards")
    time.sleep(1)
    while getAngle() < 350 and getAngle() > 100:
        if getAngle() > 350 or getAngle() < 50:
            print("broke")
            break
        global anglesAndDists
        #see if house
        print("seing houses")
        detectHouseEdges(17)
        print("saw houses")
        
        a = rightCornerDist 
        b = leftCornerDist 
        alpha = rightCornerAngle
        beta = leftCornerAngle

        anOfAprch = getAngleOfApproach(a, b, alpha, beta)

        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)

        anglesAndDists = {int(distToNextHouse) : int(anOfAprch)}

        time.sleep(1)
        leftTurn(5, 10)

    print("checked for houses")

    tankDrive.on(SpeedPercent(10), SpeedPercent(-10))
    time.sleep(1)
    tankDrive.off()

    turnRightToX(180, 10)
    print("turned back")
    time.sleep(1)
    toRemove = []
    for x in anglesAndDists:
        print("checking dists")
        print(x, anglesAndDists[x])
        turnLeftToX((anglesAndDists[x] + 90), 10)
        print("turning to angle")
        time.sleep(1)
        seenDist = dist
        if seenDist > (x-10) + 10 or seenDist < (x-10) - 10:
            print("doesnt think its right")
            toRemove.append(x)
    for x in toRemove:
        anglesAndDists.pop(x)
    toRemove.clear()

    print("checked angles and dist")
        
def getAngleOfApproach(a, b, alpha, beta):
    global anOfAprch
    try:
        anOfAprch = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
    except ZeroDivisionError:
        anOfAprch = 90
        print("fuck fuck fuck fuck FUUUUCK")
    except:
        print("wtf is wrong now?")
    return anOfAprch

def getDistToNextHouse(a, alpha, anOfAprch):
    distToNextHouse = abs(math.cos(anOfAprch - alpha)) * a
    return distToNextHouse

if __name__=="__main__":
    main()