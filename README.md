# Roborace 2024 - Solution - Teamname

A possible solution to the exercise given in the Roborace Stuttgart 2024 using the ev3dev2 Python library.

## Features

In short the robot, is programmed as a delivery robot. Detailed explanations can be found on [the homepage of the University of Stuttgart](https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/).

### main features

- drive along walls and corners (using a PID-algorithm)
- find other houses
- drive to other houses (using trigonometry)

### other features

- play sounds
- turn a number of degrees (relative to current and starting position)
- drop packages

## Credit

We want to give credit to these projects which were a great help to us.

### Operating System and library

Operating system and language bindings which are the basis of our project. https://www.ev3dev.org/docs/getting-started/

### Documentation

The library documentation. https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/index.html

### Simulation

Simulations to test code without having the ev3 at hand.

[3D Simulation](https://gears.aposteriori.com.sg/) [2D Simulation](https://www.aposteriori.com.sg/Ev3devSim/)
Config files can be found in the repository under miscellaneous

### Naming conventions

Naming conventions for both commits and code to make the the project readable.
Commit conventions: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13
Coding conventions: https://android.googlesource.com/platform/external/google-styleguide/+/refs/tags/android-s-beta-2/pyguide.md

## Code explanation

### Limitations

It should be mentioned however that the current implementation has a few drawbacks.

- First of all the robot moves rather slowly, this can be changed with a single variable but may have unforeseen consequences.
- Additionally, the PID parameters used to keep the robot orthogonal to the wall require more tweaking.
