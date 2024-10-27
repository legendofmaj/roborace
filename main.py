#!/usr/bin/env python3

from time import sleep

#import drop_packet

#For errors see: https://github.com/ev3dev/ev3dev-lang-python/issues/626
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.sensor.lego import ColorSensor

#Define modules
btn = Button()
m = LargeMotor(OUTPUT_B)

def readColorSensor():
    red = 5
    #while True: reason: a while true loop in a while true loop will get stuck
    sleep(0.2)
    colorDetected = ColorSensor.color
    if colorDetected == red:            
        seesRed  = True
        print("sees red")
        colorDetected = ColorSensor.color
    else:
        seesRed = False
        print("no red")
        colorDetected = ColorSensor.color

'''while True:
    sleep(1)
    #if btn.any():
        #print("Button pressed!")
        #m.on_for_rotations(SpeedPercent(-75), 5)     
        #sleep(1)
    #if seesRed == True:
        #drop_packet.Drop()
        #print("happy")
    #elif seesRed == False:
        #print("blind")
    read_color_sensor.readColor()'''
