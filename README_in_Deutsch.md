# Roborace 2024 - Lösung - MPG Happy Hippos

Eine mögliche Lösung zur Aufgabe des diesjährigen Roborace Stuttgart mithilfe der ev3dev2 Python Bibliothek.

![language](https://img.shields.io/badge/language-python-blue?logo=python)
[![library](https://img.shields.io/badge/library-ev3dev2-orange)](https://www.ev3dev.org)

## Funktionen

Kurz gesagt, der Roboter ist als Lieferroboter programmiert.

Detaillierte Erklärungen zur Aufgabe können im [Anhang](#Anhang) "Aufgabenstellung" und auf [der Homepage der Universität Stuttgart](https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/) gefunden werden.

### Zentrale Funktionen

- entlang von Wänden und Ecken fahren (mithilfe eines PID-Reglers)
- andere Häuser finden
- zu anderen Häusern fahren (optimaler Kurs wird mithilfe von Trigonometrie berechnet)

### Weitere Funktionen

- Töne abspielen
- unterschiedliche Gradzahl drehen (sowohl relativ zur aktuellen als auch zur ursprünglichen Position)
- Pakete abwerfen

## Code Erklärung

Die Kontrolle des Roboters erfolgt mittels mehrerer ineinander verschachtelter Schleifen und paralleler Threads.

In den Threads werden die Sensorwerte des Ultraschallsensors zur Abstandserfassung und des Gyrosensors zur Winkelerfassung ausgelesen aufbereitet und den Routinen des Hauptprogramms (main) mittels Klassen zur Verfügung gestellt.

Der Farbsensor wird direkt aus dem Hauptprogramm angesprochen.

Aus Gründen der Vereinfachung wurde auf eine zusätzliche Mittelschicht (middleware) die eine Abarbeitung in festen Zeitrastern und Bibliotheksunabhängigkeit zur Hardware ansteuerung ermöglichte verzichtet. Gleiches gilt für den Verzicht auf ein Hardware spezifisches Betriebssystem (OS, Robo-OS).

### Strategie

Der Roboter fährt an der Wand eines Hauses entlang, bis der Farbsensor eine rote Linie erkennt. Während der Fahrt versucht der Roboter mit Hilfe des Abstandsensors einen Abstand von 13cm zur Wand zu halten.
Sobald die Rote Linie detektiert wurde hält der Roboter an. Es folgt eine Drehung, die einen   Winkelbereich von ~180° abdeckt. Während der Drehung wird kontinuierlich der Abstand erfasst und ausgewertet. Über eine Kantenerkennung werden die Positionen der Ecken der in der Nähe stehenden Häuser erfasst und deren Abstände und Winkel in einem Diktionary gespeichert.
Die Wand mit dem kürzesten Abstand soll im rechten Winkel angefahren werden. Dieser Ansteuerwinkel wird mittels Cosinussatz errechnet.
Bevor die nächste Hauswand angefahren wird, wird jedoch noch das Paket abgeworfen. Damit der Roboter nicht über das abgeworfene Paket fährt, dreht er sich kirz aus der Richtung, läßt das Paket fallen und steuert dann die nächste Wand an.

### Entlang von Wänden und Ecken fahren

Folgendes ist die Grundlage für das Entlangfahren an Wänden. Es nutzt die Differenz zwischen der aktuellen Distanz zu einem Haus und der Distanz, die der Roboter haben soll, und setzt diese in eine PID-Regler-Formel ein. Der Ausgabewert wird dann zur Steuerung genutzt.

```python
error = ultrasonic_sensor.distance_centimeters - goal
integral += (error * deltaTime)
derivative = (error - previous_error) / deltaTime

turnratio = (kp * error) + (ki * integral) + (kd * derivative)

steering_drive.on(turnratio, 20)
```

Die Ermittlung der Differenz zwischen Solldistanz und

[ganze Datei](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/parallelWallDrive.py)

### Andere Häuser finden

Folgendes ist die Basis für das Erkennen von Hausecken. Es berechnet permanent die Differenz zwischen der aktuellen und der letzten Distanz und schaut nach großen Sprüngen. Wenn ein Wertesprung groß genug ist, wird eine Hausecke erkannt, und der aktuelle Winkel sowie die Distanz zum nächsten Haus wird gespeichert.

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

[ganze Datei](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/determine_angles_distances_next_house.py)

### Zu anderen Häusern fahren (mithilfe von Trigonometrie)

Folgendes ist die Formel um den Anfahrtswinkel zum nächsten Haus zu berechnen.

```python

anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
#a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle
```

<img src="https://github.com/user-attachments/assets/824af1e1-f8b9-4086-b86a-2cafe2ced7aa" width="450">

[ganze Datei](https://github.com/legendofmaj/ev3/blob/dev/AA_main_1st_round/modules/get_angle_of_approach.py)

# Anhang

## Aufgabenstellung

Die Aufgabenstellung erfolgte durch den Fachbereich des Studiengangs technische Kybernetik der Universität Stuttgart.

### Die Aufgabenstellung

Durch Industrie 4.0, individuell gefertigte Produkte und zunehmendes Onlineshopping steigt die Zahl der zu verteilenden Güter stark an. Während Industrie 4.0 und Produktion on-demand vielversprechende Möglichkeiten sind, Ressourcen effizient zu nutzen, stellen diese Entwicklungen neue Herausforderungen an die Logistik. Um diesen Herausforderungen zu begegnen und gleichzeitig umweltfreundliche Lieferketten aufzubauen, arbeiten Paketlieferdienste an autonomen Lieferfahrzeugen. Solch ein Fahrzeug soll im diesjährigen Roborace-Wettbewerb konstruiert werden. Die Aufgabe des Roboters ist es, mehrere Häuser anzufahren und dort Pakete abzuliefern. (weitere Details siehe [1])

# Literatur

[1] Aufgabenstellung Roborace 2024: in elektronischer Form als lokale Datei Aufgabenstellung_Roborace2024.pdf und auf der Internetseite der Universität Stuttgart https://www.ist.uni-stuttgart.de/de/lehre/roborace/aufgabe/Aufgabenstellung_Roborace2024.pdf

# Danksagungen

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
