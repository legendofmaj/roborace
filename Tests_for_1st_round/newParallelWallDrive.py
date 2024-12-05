#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import * #only necessary for the simulation

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

# ultrasonic_sensor_in2 = UltrasonicSensor(INPUT_2)
# ultrasonic_sensor_in3 = UltrasonicSensor(INPUT_3)
ultrasonic_sensor = UltrasonicSensor(INPUT_4)

def main():
    kp = 3
    goal = 10 #50
    while True:
        error = ultrasonic_sensor.distance_centimeters - goal
        turnratio = kp * error
        print("distance: " + str(ultrasonic_sensor.distance_centimeters))
        print("turnratio: " + str(turnratio))
        steering_drive.on(turnratio, 20)

if __name__=="__main__":
    main()
