#!/usr/bin/env python3

#https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#gyro-sensor
import time

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank

tank = MoveTank(OUTPUT_B, OUTPUT_C)

Gyro = GyroSensor(INPUT_2)

def main():
    print("has been initialized")
    Gyro.calibrate()
    time.sleep(5)
    print("calibrated")
    #Gyro.calibrate()
    #time.sleep(5)
    #Gyro.rate
    while True:
        #rate = Gyro.rate #nearly momentary as far as i can see
        circleAngle = Gyro.circle_angle() # starts at 90° when turned right by 90°goes to 360°; when rotated by 180° goes to 270°; when rotated by 270° to the right goes to 180°; when rotated by 360° to the right goes back to 90°
        #angle = Gyro.angle # when circleangle is 90 this is zero when circleangle drecreases ( robot is turned to the right) this increases proportionally with factor 1
        #print("rate: " + str(rate))
        print("circle angle: " + str(circleAngle))
        #print("angle: " + str(angle)) 
        #readAngle()
        time.sleep(1)
        '''tank.on_for_rotations(SpeedPercent(-50), SpeedPercent(50), 0.5)
        time.sleep(1)
        circleAngle = Gyro.circle_angle() # starts at 90° when turned right by 90°goes to 360°; when rotated by 180° goes to 270°; when rotated by 270° to the right goes to 180°; when rotated by 360° to the right goes back to 90°
        angle = Gyro.angle # when circleangle is 90 this is zero when circleangle drecreases ( robot is turned to the right) this increases proportionally with factor 1
        #print("rate: " + str(rate))
        print("circle angle: " + str(circleAngle))
        print("angle: " + str(angle)) 
        time.sleep(1)
        tank.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), 0.5)
        time.sleep(1)'''

def readAngle():
    circleAngle = Gyro.circle_angle()
    print(circleAngle)

if __name__=="__main__":
    main()