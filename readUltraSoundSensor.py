#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor

uSoundSensor = UltrasonicSensor(INPUT_3)
dist = 0.0

def main():
    while True:
        dist = uSoundSensor.distance_centimeters
        print(dist)
        time.sleep(1)