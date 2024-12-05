#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, LargeMotor, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

import time
import sys
import math

#Input and Output list
ultrasound_sensor_port = INPUT_3
rightMotor = OUTPUT_A
leftMotor = OUTPUT_B
gyro_sensor_port = INPUT_2
tank_drive = MoveTank(leftMotor, rightMotor)


tank_drive = MoveTank(leftMotor, rightMotor)
ultrasound_sensor = UltrasonicSensor(ultrasound_sensor_port)
gyro = GyroSensor(gyro_sensor_port)


def main():
    tank_drive.on(SpeedPercent(10), SpeedPercent(10))
    goalCm = 10
    kp = 1
    while True:
        distanceCm = ultrasound_sensor.distance_centimeters
        print("current: " + str(distanceCm))
        error = distanceCm - goalCm
        print("error: " + str(error))
        print("kp: " + str(kp))
        turnratio = error * kp
        print("turn: " + str(turnratio))
        tank_drive.turn_degrees(SpeedPercent(35), turnratio)

if __name__=="__main__":
    main()