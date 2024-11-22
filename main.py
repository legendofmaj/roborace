#!/usr/bin/env python3

#necessary libraries
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound

#other files
import sound

#input and output list
ultrasound_sensor_port = INPUT_3
color_sensor_port = INPUT_1
gyro_sensor_port = INPUT_2
rightMotor = OUTPUT_B
leftMotor = OUTPUT_C

#variables to library functions
button = Button()
tank_drive = MoveTank(leftMotor, rightMotor)
ultrasound_sensor = UltrasonicSensor(ultrasound_sensor_port)
color_sensor = ColorSensor(color_sensor_port)
gyro = GyroSensor(gyro_sensor_port)

def main():
    #Check for button input
    while True:
        if button.any() == True:
            break
    sound.firstSoundFile()
    #ToDo: drive parallel to wall (import file)
    
    #Check for color red
    while True:
        color = color_sensor.color
        if color == 5:
            #find next house
            #drop
            #go to next house
            #turn 90°
            #drive parallel to wall


if __name__ == "__main__":
    main()


                

