# "slave"

import time

from ev3dev2.motor import MediumMotor, OUTPUT_A, SpeedPercent

motorAblegen = MediumMotor(OUTPUT_A)

def Drop():
    #code to stop moving
    motorAblegen.on_for_rotations(SpeedPercent(75), 2.25)
    time.sleep(0.5)
    motorAblegen.on_for_rotations(SpeedPercent(75), -2.25)