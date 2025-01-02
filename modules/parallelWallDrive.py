#!/usr/bin/env python3

# Import the necessary libraries
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import math
import time

from turning import *
import angles_dists_thread

#from ev3dev2.sensor.virtual import * #only necessary for the simulation

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_C)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_C, OUTPUT_B)

#ultrasonic_sensor = UltrasonicSensor(INPUT_3)
color_sensor = ColorSensor(INPUT_1)

diststart=17
distarryx=(list(range(0,360)))
distarry=(list(range(0,360)))
mind=1000000
minphi=1000000
mindavg=1000000
minphiavg=1000000

def main():
    #values for pid tuning
    kp = 1.0
    ki = 0.2
    kd = 0.2

    #other values for tuning
    goal = 13#cm

    #define other important values
    integral = 0
    previous_error = 0
    deltaTime = 0
    stopint = 1
    countx = 0
    countd = 0
    countv = 0
    previous_time = time.time()
    time.sleep(0.01) #a quick break, to not get a zero division error

    while True:
        current_time = time.time()
        deltaTime = current_time - previous_time
        
        errorv = angles_dists_thread.threadOutput.dist - goal
        integral += stopint*(errorv * deltaTime)
        derivative = (errorv - previous_error) / deltaTime

        if (abs(errorv)>10.0):
            kp=0.2
        else:
            kp=1.0
        
        if (abs(derivative)>100):
            kd=1.0
            ki=0.02
            stopint=0
            countd+=1
        elif ((countd>0)and(countd<4)):    
            countd+=1
        else:
            kd=0.2 
            ki=0.2
            stopint=1
            countd=0

        turnratio = (kp * errorv) + (ki * integral) + (kd * derivative)
        turnratio_o = turnratio
        #limit to safe values
        if turnratio > 25:
            turnratio = 25
            if ( (errorv - previous_error)>0):
                countv+=1
        elif turnratio < -100:
            turnratio = -100
            
        if countv>20:
            turnratio = 0
            for i in distarryx:
                distarry[i]= 20+15.0*(1-(math.sin(i*math.pi/360)*math.sin(i*math.pi/360)))

            swipelr(170)
            print("------------ mind Avg:",mindavg)
            print("------------ minphi Avg:",minphiavg)

            print("turning left absolut")

            turn_to_x_left(minphiavg,10.0)
            time.sleep(1)
            countv=0

        print("distance: " + str(angles_dists_thread.threadOutput.dist) + "     error: "+str(errorv))
        print("turnratio calculated: " + str(turnratio_o))
        print("turnratio limited: " + str(turnratio) + " countv: " + str(countv)+ " countd: " + str(countd))
        print("deltaTime: " + str(deltaTime) + "    deriv: " + str(derivative))
        steering_drive.on(turnratio, -20)
        previous_error = errorv
        previous_time = current_time
        checked_color = checkColor()
        if checked_color[0] == True:
            return checked_color
        


def checkColor():
    colorSeen = [
        False,
        False,
        False
    ]
    rawColor = color_sensor.color
    col_raw = color_sensor.raw
    if rawColor == 5:
        colorSeen[1] = True
        colorSeen[0] = True
        colorSeen[2] = False
    elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
        colorSeen[0] = True
        colorSeen[2] = True
        colorSeen[1] = False
    return colorSeen


def swipelr():
    global distarry
    global mind
    global minphi
    global mindavg
    global minphiavg
    print("swiping left")

    relswiper(90, 10.0)

    time.sleep(1)

    lmind=mind
    lphi=minphi

    print("swiping right")

    relswipel(120, 10.0)
    time.sleep(1)
    mindavg=(mind+lmind)/2
    minphiavg=(minphi+lphi)/2
    print("mind l:",lmind,"mind r:",mind,"mind Avg:",mindavg)
    print("minphi l:",lphi,"mind r:",minphi,"mind Avg:",minphiavg)

    turn_to_x_right(minphiavg, 10)

def relswipel(degrees, speed):
    global distarry
    global mind
    global minphi
    cpos = angles_dists_thread.threadOutput.circleAngle
    target = cpos + degrees
    print("relturnv.target:",target)
    tolerance=5
    if (target<360):
        while angles_dists_thread.threadOutput.circleAngle < target-tolerance:
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            print("relturnv.circleAngle1:", angles_dists_thread.threadOutput.circleAngle) 
            dphi=distarry[int(angles_dists_thread.threadOutput.circleAngle)]
            print("distance:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=angles_dists_thread.threadOutput.circleAngle
        print("relturnv.Done1")
    else:
        npos=0
        while ((angles_dists_thread.threadOutput.circleAngle+npos<target-tolerance)):
            tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
            time.sleep(0.1)
            if angles_dists_thread.threadOutput.circleAngle<cpos:
                npos=360
            print("relturnv.circleAngle2:", angles_dists_thread.threadOutput.circleAngle) 
            dphi=distarry[int(angles_dists_thread.threadOutput.circleAngle)]
            print("distance:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=angles_dists_thread.threadOutput.circleAngle
        print("relturnv.Done2")
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnv.Done3")
    print("minphi:",minphi,"mind:",mind)

def relswiper(degrees, speed):
    global distarry
    global mind
    global minphi

    cpos = angles_dists_thread.threadOutput.circleAngle
    target = cpos - degrees
    print("relswiper.target:",target)
    tolerance=5
    if (target>0):
        while angles_dists_thread.threadOutput.circleAngle > target+tolerance:
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            print("relswiper.circleAngle1:", angles_dists_thread.threadOutput.circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(angles_dists_thread.threadOutput.circleAngle)]
            print("relswiper.distance1:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=angles_dists_thread.threadOutput.circleAngle
        print("relswiper.Done1")
    else:
        npos=0
        while ((angles_dists_thread.threadOutput.circleAngle-npos>target+tolerance)):
            tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
            time.sleep(0.1)
            if cpos-angles_dists_thread.threadOutput.circleAngle<0:
                npos=360
            print("relswiper.circleAngle2:", angles_dists_thread.threadOutput.circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(angles_dists_thread.threadOutput.circleAngle)]
            print("relswiper.distance2:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=angles_dists_thread.threadOutput.circleAngle
        print("relswiper.Done2")
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    print("relswiper.Done3")
    print("minphi:",minphi,"mind:",mind)   