#!/usr/bin/env python3
"""main module of the project"""

import time
import threading

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential
from ev3dev2.button import Button
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound


import modules.angles_dists_thread
import modules.parallel_wall_drive
import modules.turning

STUD_MM = 7
STUDS_THAT_WHEELS_ARE_APART = 15
MIN_DIST_BETWEEN_WHEELS = 118 #mm
moveDifferential = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3EducationSetTire, STUDS_THAT_WHEELS_ARE_APART * STUD_MM)


tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
gyroSensor = GyroSensor(INPUT_2)

stop_event = threading.Event()

col_raw = [
    0,
    0,
    0
]

POS_O = 90
ZERO = 90

time.sleep(0.3)

def main():
    """function containing the main code of the project"""
    print("please press")
    modules.angles_dists_thread.start_threads()
    global ZERO
    ZERO = modules.angles_dists_thread.ThreadOutput.circle_angle

    Sound().play_file('/home/robot/ev3/miscellaneous/soundFiles/Audio1.wav', volume=100, play_type=0)

    while True:
        if Button().any():
            break
        time.sleep(0.05)
    global POS_O
    POS_O = modules.angles_dists_thread.ThreadOutput.circle_angle
    ZERO = 90

    tankDrive.on_for_rotations(SpeedPercent(-10), SpeedPercent(-10), 1)
    time.sleep(0.5)
    color = [
        False,
        False,
        False
    ]
    while True:
        color = modules.parallel_wall_drive.main()
        if color[1]:
            print("red")
            tankDrive.off()

            POS_O = modules.angles_dists_thread.ThreadOutput.circle_angle

            angles_and_dists = modules.detect_houses_primitive.getHousePrimitive()

            wanted_an_of_aprch = int(float(angles_and_dists[modules.detect_houses_primitive.dist_short]))

            modules.turning.turn_to_x_right(50, 10)
            drop()
            time.sleep(0.5)
            print("checking dists")
            modules.turning.turn_to_x_left((wanted_an_of_aprch + 90), 10)
            print("turning to angle")
            time.sleep(0.2)

            to_drive_dist = modules.detect_houses_primitive.dist_short - 13
            if to_drive_dist > 5:
                drive_till_dist_wheel(to_drive_dist)
                print("drove")

            modules.turning.relative_turnv(90, 10)
            time.sleep(0.2)
            POS_O = modules.angles_dists_thread.ThreadOutput.circle_angle

        if color[2]:
            tankDrive.off()
            print("green")
            smooth_drive_straight(20)
            time.sleep(3)
            tankDrive.off()
            break


def drop():
    """function to drop the parcel"""
    print("dropping")
    depositMotor.on_for_rotations(SpeedPercent(75), 1.75)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -1.75)

def drive_straight(speed, rotations):
    """function to drive forward for a specified number of rotations"""
    tankDrive.on_for_rotations(SpeedPercent(-speed), SpeedPercent(-speed), rotations)

def smooth_drive_straight(speed):
    """function to drive forward"""
    tankDrive.on(SpeedPercent(-speed), SpeedPercent(-speed))

def drive_till_dist_wheel(dist):
    """function to drive a specified distance"""
    rotations = 0.00
    rotation = 0.01
    while True:
        tankDrive.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), rotation)
        rotations += rotation
        dist_crossed = rotations * 22.3 #in cm
        if dist_crossed >= dist:
            break


if __name__=="__main__":
    main()
# End-of-file (EOF)