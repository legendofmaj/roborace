#!/usr/bin/env python3

# Import the necessary libraries
import time
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev2.sensor.virtual import * #only necessary for the simulation

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_C)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_C, OUTPUT_B)
color_sensor = ColorSensor(INPUT_1)
ultrasonic_sensor = UltrasonicSensor(INPUT_3)

def main():
    #values for pid tuning
    kp = 1.0
    ki = 0.1
    kd = 0.1

    #other values for tuning
    goal = 13#cm

    #define other important values
    integral = 0
    previous_error = 0
    deltaTime = 0
    previous_time = time.time()
    time.sleep(0.01) #a quick break, to not get a zero division error

    while True:
        current_time = time.time()
        deltaTime = current_time - previous_time
        
        error = ultrasonic_sensor.distance_centimeters - goal
        integral += (error * deltaTime)
        derivative = (error - previous_error) / deltaTime

        turnratio = (kp * error) + (ki * integral) + (kd * derivative)

        #limit to safe values
        if turnratio > 12.5:
            turnratio = 12.5
        elif turnratio < -12.5:
            turnratio = -12.5

        print("distance: " + str(ultrasonic_sensor.distance_centimeters))
        print("turnratio: " + str(turnratio))
        print("deltaTime: " + str(deltaTime))
        steering_drive.on(turnratio, -20)
        previous_error = error
        previous_time = current_time

        if checkColor() == True:
            break

def checkColor():
    colorSeen = False
    rawColor = color_sensor.color
    col_raw = color_sensor.raw
    rawColor = color_sensor.color
    col_raw = color_sensor.raw
    if rawColor == 5:
        colorSeen = True
    elif (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
        colorSeen = True
    return colorSeen

if __name__=="__main__":
    main()
