import math

#trying to figure out how to alternativly determine driven distance or angle

wheel_rotations = 0.0
wheel_radius = 22.3 #cm
U_wheel = math.pi*wheel_radius*2
dist_calc = wheel_rotations*U_wheel




# trying to figure out how  much the robot has turned based on turn circumference and turned distance !!!attention very inaccurate mesurment!!!
min_dist_between_wheels = 11.8 #cm
min_dist_to_middle = 5.9 #cm
max_dist_between_wheels = 18.8 #cm
max_dist_to_middle = 9.4 #cm

#defining turn radius as middle of min and max distance to middle

turn_radius = (min_dist_to_middle + max_dist_to_middle)/2
turn_circumference = 2* math.pi * turn_radius

#measured angle will be in ratio of distance the wheel crossed and total turn circumferance

turn_dist_turn_circumferance_ration =  dist_calc/turn_circumference

# thus the angle change in degreesis that ration multiplied by 360°

turn_angle = turn_dist_turn_circumferance_ration*360

#please note that all of this is somewhat janky as it does not take into account in which direction the wheel rotates