#!/usr/bin/env python3

import time

#necessary libraries
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound

#other files
import modules.sound

#input and output list
ultrasound_sensor_port = INPUT_3
color_sensor_port = INPUT_1
gyro_sensor_port = INPUT_2
rightMotor = OUTPUT_B
leftMotor = OUTPUT_C

#variables to library functions
# button = Button()
# tank_drive = MoveTank(leftMotor, rightMotor)
# ultrasound_sensor = UltrasonicSensor(ultrasound_sensor_port)
# color_sensor = ColorSensor(color_sensor_port)
# gyro = GyroSensor(gyro_sensor_port)

def main():
    modules.sound.firstSoundFile()
    time.sleep(1)
    modules.sound.secondSoundFile()

if __name__ == "__main__":
    main()