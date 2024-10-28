#!/usr/bin/env python3

#https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#gyro-sensor
import time

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

Gyro = GyroSensor(INPUT_2)

def main():
    print("has been initialized")
    #Gyro.rate
    while True:
        #rate = Gyro.rate #nearly momentary as far as i can see
        circleAngle = Gyro.circle_angle() # starts at 90° when turned right by 90°goes to 360°; when rotated by 180° goes to 270°; when rotated by 270° to the right goes to 180°; when rotated by 360° to the right goes back to 90°
        #angle = Gyro.angle # idk what this rlly does its strange starts at -35° but goes all over the place
        #print("rate: " + str(rate))
        print("circle angle: " + str(circleAngle))
        #print("angle: " + str(angle)) 
        time.sleep(1)



main()