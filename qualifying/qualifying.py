#!/usr/bin/env python3

#Warning: dependencies of this file are determine_angles_distances_next_house.py, driving.py, drop_packet.py, get_angle_of_approach.py, sound.py and turning.py
#This file will not work without the mentioned dependencies

import time
import threading

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound

import modules

btn = Button()
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
color_sensor = ColorSensor(INPUT_1)
gyro_sensor = GyroSensor(INPUT_2)
ultrasound_sensor = UltrasonicSensor(INPUT_3)
speaker = Sound()

col_raw = [0, 0, 0]
min_dist_to_house = 12

gyro_sensor.reset()
def main():
    start_threads()
    modules.sound.firstSoundFile()

    #Start driving when any button on the ev3 is pressed
    while True:
        if buttonPressed == True:
            break
        time.sleep(0.05)

    #Drive until the red line is reached
    while True:
        if color == "red":
            print("saw red")
            break
        modules.driving.driveStraight(10)
    modules.driving.driveStraight(0)
    #determine geometrics
    modules.determine_angles_distances_next_house.main()

    #Drop the package
    modules.drop_packet.main()    


    #get angle of approach 
    #Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
    a = modules.determine_angles_distances_next_house.importantValues.rightCornerDist
    b = modules.determine_angles_distances_next_house.importantValues.leftCornerDist
    alpha = modules.determine_angles_distances_next_house.importantValues.rightCornerAngle
    beta = modules.determine_angles_distances_next_house.importantValues.leftCornerAngle

    anOfAprch = modules.get_angle_of_approach.getAngleOfApproach(a, b, alpha, beta)
    print(anOfAprch)

    #turn toward house
    modules.turning.turnLeftToX(anOfAprch, 10)
    #Drive until a tbd distance to the next house and turn by 90° degrees
    modules.driving.driveTillDist(min_dist_to_house)
    modules.turning.leftTurn(90, 15)

    #Drive until the green line is reached
    while True:
        if (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            break
        modules.driving.driveStraight(20)
    time.sleep(3)
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    modules.sound.secondSoundFile()
    

class distance:
    dist = 0.0

def start_threads():
    buttonThread = threading.Thread(target = read_button)
    buttonThread.daemon = True
    buttonThread.start()
    colorThread = threading.Thread(target = read_color)
    colorThread.start()

def read_button():
    global buttonPressed
    buttonPressed = False
    while True:
        if btn.any() == True:
            buttonPressed = True
            time.sleep(0.05)
            break

def read_color():
    global color
    global col_raw
    color = "none"
    col_raw = color_sensor.raw
    rawColor = color_sensor.color
    while True:
        col_raw = color_sensor.raw
        rawColor = color_sensor.color
        if rawColor == 5:
            color = "red"
        elif rawColor == 3:
            color = "green"
        time.sleep(0.1)

def read_dist():
    while True:
        distance.dist = ultrasound_sensor.distance_centimeters
        time.sleep(0.1)

def readcircle_angle():
    global circle_angle
    while True:
        circle_angle = gyro_sensor.circle_angle()
        time.sleep(0.05)

if __name__=="__main__":
    main()