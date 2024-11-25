import time
import threading 
import sys
import math

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor, Motor, MoveDifferential, SpeedRPM
from ev3dev2.button import Button
from ev3dev2.wheel import EV3Tire, EV3EducationSetTire# i think the latter tire is the one we are using

tankDrive = MoveTank(OUTPUT_B, OUTPUT_C)
tankDrive.gyro = GyroSensor(INPUT_2)
btn = Button()
depositMotor = MediumMotor(OUTPUT_A)
motorRight = Motor(OUTPUT_B)
motorLeft = Motor(OUTPUT_C)
colorSensor = ColorSensor(INPUT_1)
gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
tankDrive.gyro = gyroSensor

circleAngle = 90

stop_event = threading.Event()

gyroSensor.reset()
tankDrive.gyro.reset()

def readCircleAngle():
    global circleAngle
    while not stop_event.is_set():
    #while True:
        circleAngle = gyroSensor.circle_angle()
        time.sleep(0.05)
        #print(circleAngle)
    print("is set")

def main():
    circleAngleThread = threading.Thread(target = readCircleAngle, args=(stop_event))
    circleAngleThread.start()

    print(circleAngle)
    tankDrive.turn_degrees(SpeedPercent(-10), 90)

    time.sleep(1)

    tankDrive.turn_degrees(SpeedPercent(-10), -90)

    stop_event.set()
    circleAngleThread.join()
    gyroSensor.reset()
    tankDrive.gyro.reset()
    time.sleep(1)

    tankDrive.turn_degrees(SpeedPercent(-10), 90)

    time.sleep(1)

    tankDrive.turn_degrees(SpeedPercent(-10), -90)
    
    stop_event.clear()
    circleAngleThread = threading.Thread(target = readCircleAngle)
    circleAngleThread.start()

    tankDrive.turn_degrees(SpeedPercent(-10), 90)

    time.sleep(1)

    tankDrive.turn_degrees(SpeedPercent(-10), -90)