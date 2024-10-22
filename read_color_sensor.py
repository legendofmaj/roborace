# "slave"
#!/usr/bin/env python3s

from time import sleep

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor import ColorSensor

colorToExport = ColorSensor.color()