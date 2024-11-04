#!/usr/bin/env python3

import time

from ev3dev2.motor import MediumMotor, OUTPUT_A, SpeedPercent

depositMotor = MediumMotor(OUTPUT_A)

def Drop():
    #code to stop moving
    depositMotor.on_for_rotations(SpeedPercent(75), 2.25)
    time.sleep(0.5)
    depositMotor.on_for_rotations(SpeedPercent(75), -2.25)
    time.sleep(0.5)
    #code to resume other programms