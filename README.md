# Roborace 2024 - possible solution

A possible solution to the exercise given in the Roborace Stuttgart 2024 using the ev3dev2 Python library.

![language](https://img.shields.io/badge/language-python-blue?logo=python)
[![library](https://img.shields.io/badge/library-ev3dev2-orange)](https://www.ev3dev.org)

[Readme in Deutsch](https://github.com/legendofmaj/ev3/blob/main/miscellaneous/README_in_Deutsch.md)
[Bericht in Deutsch](https://github.com/legendofmaj/ev3/blob/final_refactor/miscellaneous/report/Bericht_in_Deutsch.md)
## Features

In short, the robot is programmed as a delivery robot. Detailed explanations can be found on [the homepage of the University of Stuttgart](https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/).

### Main features

- drive along walls and corners (using a PID controller)
- find other houses
- move to other houses (using trigonometry)

### Other features

- play sounds
- turn a number of degrees (relative to current and start position)
- drop packages

## Code explanation

### Drive along walls and corners

This is the basis for the robot driving along the wall. It uses the the difference between the current distance to a house and the distance it is supposed to have and plugs it into a PID controller formula. The output value is then used for steering the robot.

```python
error = ultrasonic_sensor.distance_centimeters - goal
integral += (error * deltaTime)
derivative = (error - previous_error) / deltaTime

turnratio = (kp * error) + (ki * integral) + (kd * derivative)

steering_drive.on(turnratio, 20)
```

[entire file](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/parallelWallDrive.py)

### Find other houses

This is the basis for dectecting the edges of houses. It constantly calculates the difference between the current and the last distance and looks for large jumps. If a jump is large enough, a house edge is detected and the current angle and distance are stored.

```python
while True:
  distOld = ultraSoundSensor.distance_centimeters
  distNew = ultraSoundSensor.distance_centimeters
  if abs(distOld-distNew) >= threshold and distNew < 100:           
  importantValues.rightCornerAngle = gyroSensor.circle_angle() 
  importantValue.rightCornerDist = distNew
  break
  #repeat for left side
```
[entire file](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/determine_angles_distances_next_house.py)

### Drive to other houses using trigonometry

This is the formula for calculating the angle of approach to the next house.

```python

anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
#a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
```

<img src="https://github.com/user-attachments/assets/824af1e1-f8b9-4086-b86a-2cafe2ced7aa" width="450">

[entire file](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/get_angle_of_approach.py)

## Credit

We would like to give credit to these projects that helped us a lot.

### Operating system and library

Operating system and language bindings that form the basis of our project. https://www.ev3dev.org/docs/getting-started/

### Documentation

The library documentation. https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/index.html

### Simulation

Simulations to test code without having the ev3 at hand.

[3D Simulation](https://gears.aposteriori.com.sg/) [2D Simulation](https://www.aposteriori.com.sg/Ev3devSim/)

> Config files can be found in the repository under miscellaneous

### Naming conventions

Naming conventions for both commits and code to make the the project readable.

Commit conventions: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13

Coding conventions: https://android.googlesource.com/platform/external/google-styleguide/+/refs/tags/android-s-beta-2/pyguide.md
