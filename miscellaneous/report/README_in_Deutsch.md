# Roborace 2024 - Lösung - MPG Happy Hippos

Eine mögliche Lösung zur Aufgabe des diesjährigen Roborace Stuttgart mithilfe der ev3dev2 Python Bibliothek.

![language](https://img.shields.io/badge/language-python-blue?logo=python)
[![library](https://img.shields.io/badge/library-ev3dev2-orange)](https://www.ev3dev.org)

## Funktionen

Kurz gesagt, der Roboter ist als Lieferroboter programmiert. Detaillierte Erklärungen können auf [der Homepage der Universität Stuttgart](https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/) gefunden werden.

### Zentrale Funktionen

- entlang von Wänden und Ecken fahren (mithilfe eines PID-Reglers)
- andere Häuser finden
- zu anderen Häusern fahren (mithilfe von Trigonometrie)

### Weitere Funktionen

- Töne abspielen
- unterschiedliche Gradzahl drehen (sowohl relativ zur aktuellen als auch zur ursprünglichen Position)
- Pakete abwerfen

## Code Erklärung

### Entlang von Wänden und Ecken fahren

Folgendes ist die Grundlage für das Entlangfahren an Wänden. Es nutzt die Differenz zwischen der aktuellen Distanz zu einem Haus und der Distanz, die der Roboter haben soll, und setzt diese in eine PID-Regler-Formel ein. Der Ausgabewert wird dann zur Steuerung genutzt.

```python
error = ultrasonic_sensor.distance_centimeters - goal
integral += (error * deltaTime)
derivative = (error - previous_error) / deltaTime

turnratio = (kp * error) + (ki * integral) + (kd * derivative)

steering_drive.on(turnratio, 20)
```
[ganze Datei](../../modules/parallel_wall_drive.py?#L31)

### Andere Häuser finden

Folgendes ist die Basis für das Erkennen von Hausecken. Es berechnet permanent die Differenz zwischen der aktuellen und der letzten Distanz und schaut nach großen Sprüngen. Wenn ein Wertesprung groß genug ist, wird eine Hausecke erkannt, und der aktuelle Winkel sowie die Distanz zum nächsten Haus wird gespeichert.

```python
while ThreadOutput.circle_angle < 350 and ThreadOutput.circle_angle > 100:
  if dist_old > dist_new:
    if dist_short > dist_new:
      dist_short = dist_new
      angle_short = angle_new
angles_and_dists = {int(dist_short) : int(angle_short)}
return angles_and_dists
```
[ganze Datei](../../modules/detect_houses_primitive.py?#L40)

### Zu anderen Häusern fahren (mithilfe von Trigonometrie)

Folgendes ist die Formel um den Anfahrtswinkel zum nächsten Haus zu berechnen.

```python

anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
#a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
```

<img src="../resources/Trigonometry_Sketch.png" width="450">

[ganze Datei](../../modules/detect_houses_advanced.py?#L190)

## Danksagungen

Wir möchten folgenden Projekten danken, welche eine große Hilfe für uns waren.

### Betriebssystem und Bibliothek

Betriebssystem und Bibliothek, welche die Grundlage für unser Projekt darstellen. https://www.ev3dev.org/docs/getting-started/

### Dokumentation

Die Bibliotheksdokumentation. https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/index.html

### Simulation

Simulationen, um das Programm zu testen, ohne den ev3 physisch nutzen zu können.

[3D Simulation](https://gears.aposteriori.com.sg/) [2D Simulation](https://www.aposteriori.com.sg/Ev3devSim/)

> Konfigurationsdateien können im Repository unter miscellaneous gefunden werden.

### Namensgebungskonventionen

Namensgebungskonventionen für sowohl Commits als auch den Quellcode, um das Projekt lesbar zu halten.

Commitkonventionen: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13

Programmierkonventionen: https://android.googlesource.com/platform/external/google-styleguide/+/refs/tags/android-s-beta-2/pyguide.md
