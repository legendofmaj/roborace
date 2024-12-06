#!/usr/bin/env python3

# Import the necessary libraries
import time
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import modultwo
#from ev3dev2.sensor.virtual import * #only necessary for the simulation

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_C)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_C, OUTPUT_B)

ultrasonic_sensor = UltrasonicSensor(INPUT_3)
color_sensor = ColorSensor(INPUT_1)

diststart=17
circleAngle=0.0
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
        
        errorv = ultrasonic_sensor.distance_centimeters - goal
        integral += stopint*(errorv * deltaTime)
        derivative = (errorv - previous_error) / deltaTime

        if (abs(errorv)>10.0):
            kp=0.2
       #     countx+=1
       # elif ((countx>0)and(countx<4)):
       #     countx+=1
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

#""" 
#        if ((abs(errorv)>10.0)or(abs(derivative)>100)) :
#            kd=1.0
#            ki=0.02
#            stopint=0
#        else:
#            kp=1.0
#            kd=0.2 
#            ki=0.2
#            stopint=1
# """

        turnratio = (kp * errorv) + (ki * integral) + (kd * derivative)
        turnratio_o = turnratio
        #limit to safe values
        if turnratio > 25:
            turnratio = 25
            if ( (errorv - previous_error)>0):
                countv+=1
        elif turnratio < -100:
            turnratio = -100

        #if ( (errorv>10.0) and (previous_error>10.0) and ((errorv - previous_error)>0) ):
        #    countx+=1

            
        if (countv>20) :
            turnratio = modultwo.main()#-100
            countv=0

        print("distance: " + str(ultrasonic_sensor.distance_centimeters) + "     error: "+str(errorv))
        print("turnratio calculated: " + str(turnratio_o))
        print("turnratio limited: " + str(turnratio) + " countv: " + str(countv)+ " countd: " + str(countd))
        print("deltaTime: " + str(deltaTime) + "    deriv: " + str(derivative))
        steering_drive.on(turnratio, -20)
        previous_error = errorv
        previous_time = current_time
        checked_color = checkColor()
        if checked_color[0] == True:
            return checked_color
            break

def checkColor():
    colorSeen = [False , False, False]
    rawColor = color_sensor.color
    col_raw = color_sensor.raw
    rawColor = color_sensor.color
    col_raw = color_sensor.raw
    if rawColor == 5:
        colorSeen[1] = True
        colorSeen[0] = True
    elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
        colorSeen[0] = True
        colorSeen[2] = True
    return colorSeen


if __name__=="__main__":
    main()
