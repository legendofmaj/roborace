

import time

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

Gyro = GyroSensor(INPUT_2)

def main():
    while True:
        rate = Gyro.rate
        circleAngle = Gyro.circle_angle()
        angle = Gyro.angle
        print("rate: " + str(rate))
        print("circle angle: " + str(circleAngle))
        print("angle: " + str(angle))