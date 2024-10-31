#!/usr/bin/env python3

#https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#ultrasonic-sensor
import time
import threading

from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor

uSoundSensor = UltrasonicSensor(INPUT_3)
dist = 0.0

def main():
    distThread = threading.Thread(target=readDist)
    distThread.start()
    print("scanning")
    while True:
        print(dist)
        time.sleep(0.5) 

def readDist():
    global dist
    while True:
        dist = uSoundSensor.distance_centimeters #distance in centimeters
        time.sleep(0.1)

if __name__=="__main__":
    main()