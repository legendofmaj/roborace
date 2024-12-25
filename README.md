# Roborace 2024

This repository contains a possible solution to the exercise given in the Roborace Stuttgart 2024 using the ev3dev2 Python library.

## The exercise

### What should the robot do?

In short the ev3, is supposed to be programmed as a delivery robot. It should deliver a parcel to houses that are marked with a red line without bumping into anything. Detailed explanations can be found on [the homepage of the University of Stuttgart](https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/).

The Roborace was divided into several tasks. Specifically the qualification and the main event.

- For the qualifying the robot should simply drive along a house, search for another house, drive to the 2nd house and then drive along it’s wall until a line is reached. This code along with the necessary explanations can be found [here](https://github.com/legendofmaj/ev3/releases/tag/qualifying).
- For the main event, the task was a little more complex, as there were more houses involved and the house walls weren’t straight. The code for the main event can be found [here](https://github.com/legendofmaj/ev3).

## Further reading

### Operating System
In order to use the ev3dev2 library, a third party operating system is required. Installation instructions can be found here: https://www.ev3dev.org/docs/getting-started/

### Documentation
The library documentation can be found here: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/index.html

### Simulation
To test if the code works without having the ev3 at hand, these simulations can be used: [3D Simulation](https://gears.aposteriori.com.sg/)
[2D Simulation](https://www.aposteriori.com.sg/Ev3devSim/)
Config files can be found in the repository under miscellaneous 

### Naming conventions
Naming conventions for both commits and variables/functions are important to make the code readable.
Commit conventions: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13
Variable/function conventions: https://android.googlesource.com/platform/external/google-styleguide/+/refs/tags/android-s-beta-2/pyguide.md

## Code explanation

### Limitations

It should be mentioned however that the current implementation has a few drawbacks. 

- First of all the robot moves rather slowly, this can be changed with a single variable but may have unforeseen consequences.
- Additionally, the PID parameters used to keep the robot orthogonal to the wall require more tweaking.
