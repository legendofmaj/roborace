#!/usr/bin/env python3

#https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#gyro-sensor
import time

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

Gyro = GyroSensor(INPUT_2)

def main():
    print("has been initialized")
    Gyro.rate
    while True:
        rate = Gyro.rate
        circleAngle = Gyro.circle_angle()
        angle = Gyro.angle
        print("rate: " + str(rate))
        print("circle angle: " + str(circleAngle))
        print("angle: " + str(angle))
        time.sleep(10)



main()