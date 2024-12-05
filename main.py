#!/usr/bin/env python3

#necessary libraries
import time
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound

#other files
import modules.sound
import modules.driving
import modules.turning
import modules.determine_angles_distances_next_house
import modules.drop_packet
import modules.oldParallelWallDrive

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

#variables to change
min_dist_to_house = 12

def main():
    #Check for button input
    while True:
        if button.any() == True:
            break
    #play sound
    modules.sound.startingFanfare()
    

    #drive until red line
    while True:
        color = color_sensor.color #not final
        if color == 5:
            break

        #drive parallel to wall
        modules.oldParallelWallDrive.main() #not final
        modules.driving.driveStraight(15)
    modules.driving.driveStraight(0)
   
   
    #find next house
    modules.determine_angles_distances_next_house.main() #not final

    
    #drop
    modules.drop_packet.drop()


    #go to next house

    #get angle of approach
    #Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
    a = modules.determine_angles_distances_next_house.importantValues.rightCornerDist
    b = modules.determine_angles_distances_next_house.importantValues.leftCornerDist
    alpha = modules.determine_angles_distances_next_house.importantValues.rightCornerAngle
    beta = modules.determine_angles_distances_next_house.importantValues.leftCornerAngle
    anOfAprch = modules.get_angle_of_approach.getAngleOfApproach(a, b, alpha, beta)

    #turn toward house
    modules.turning.turnLeftToX(anOfAprch, 10) #not final
    #drive until a dist to the house
    modules.driving.driveTillDist(min_dist_to_house)
    #turn 90°
    modules.turning.turnLeftToX(90, 15) #not final
    #drive parallel to wall
    modules.oldParallelWallDrive.main() #not final
    modules.driving.driveStraight(15) #not final

    #Check for corner
    #turn around corner
    #drive parallel to wall

    #Check for color green
    while True:
        col_raw = color_sensor.raw
        if (col_raw[0]*2) < col_raw[1] and (col_raw[2]*2) < col_raw[1]:
            break
        #drive for 3 seconds
        modules.driving.driveStraight(20)
    time.sleep(3)
    tank_drive.off()
    #play sound
    modules.sound.finishFanfare()

if __name__ == "__main__":
    main()            