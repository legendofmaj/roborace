#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor.lego import UltrasonicSensor

#Input and Output list
ultrasound_sensor_port = INPUT_3
rightMotor = OUTPUT_A
leftMotor = OUTPUT_B

tank_drive = MoveTank(leftMotor, rightMotor)
ultrasound_sensor = UltrasonicSensor(ultrasound_sensor_port)
#Key variable
desired_dist = 15

def main():
    # while True:
    #     if read_button() == True:
    #         break
    while True:
        print(read_dist()) #debug only
        drive(5)
        check_dist(read_dist(), desired_dist)

def read_button():
    buttonPressed = False
    while True:
        if Button().any() == True:
            buttonPressed = True
            return buttonPressed
        
def read_dist():
    while True:
        dist = ultrasound_sensor.distance_centimeters
        return dist
    
def drive(speed):
    tank_drive.on(SpeedPercent(speed), SpeedPercent(speed)) #Replace with -speed on real robot

def check_dist(current_dist, desired_dist):
    #Note: If distance is correct it is 0, if it is too big it is 1, if it is too small it is -1
    correct = 0
    if current_dist > desired_dist:
        print("dist too big")
        correct = 1
        #turn right
    elif current_dist < desired_dist:
        #turn left
        print("dist too small")
        correct = -1
    return correct

if __name__=="__main__":
    main()