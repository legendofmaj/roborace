**EV3 - Cheat Sheet**



**[Git Installieren](https://git-scm.com/)**

1. Git.exe von der verlinkten Website herunterladen 

- bei Windows unter Download for Windows auf Click Download here ganz oben drücken

2. Installer als Admin ausführen

- Unter **select components** und **Windows explorer integration** **Open Git GUI** **nicht** aktivieren, da es meist nicht verwendet wird und das Menü unsauber macht
- Unter **select default editor** ist besser anstelle von vim VS Code zu verwenden, da wir es später so oder so brauchen
- Unter adjust the name of the initial branch in new repositories override the default branch auswählen und main in die Textbox eingeben
- Bei allem hier nicht angegebenen einfach die Standard einstellungen verwenden



**Git einrichten**

1. In den Ordner gehen wo das Projekt letzendlich sein soll e.g.: Home/documents/Roborace und open **Git Bash here** drücken

```javascript
git config --global user.name "Dein GitHub Benutzername"
```

```javascript
git config --global user.email "Deine GitHub E-Mail"
```

```javascript
git init
```

```javascript
git pull https://github.com/legendofmaj/ev3.git
```

2. Git zum ersten mal verwenden

```javascript
git status
```

```javascript
git add .
```

```javascript
git commit -m "Was du verändert hast"
```

```javascript
git remote add origin https://github.com/legendofmaj/ev3.git //Nur beim ersten mal
```

```javascript
git push --set-upstream origin main //Nur beim ersten mal
```

```javascript
git push
```

3. Änderungen machen

```javascript
git status
```

```javascript
git add .
```

```javascript
git commit -m "Was du verändert hast"
```

```javascript
git push
```

**[Vorbereitung](https://www.ev3dev.org/docs/getting-started/)**

1. [Netzwerkverbindung einrichten](https://www.ev3dev.org/docs/networking) (Achtung: Dies muss später vielleicht durch Bluetooth ersetzt werden)

- Unter Windows 11 wird man nachdem man im Control Panel auf Devices and Printers geht in die Einstellungs-App verwiesen, hier muss man auf "erweiterte Einstellung", ganz unten auf der Seite gehen, um wieder ins Control Panel zu kommen.
- Das Umbenennen des ev3 funktioniert nur mit f5 in einem der Netzwerk Menüs.
- Unter Linux sollte man darauf achten unbedingt den **"nm-connection-editor"** zu verwenden.

2. [SSH Verbindung](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/)

- In PUTTY auf Windows einfach den Hostname, also **"robot"** im Feld eingeben. Bei dem SSH Passwort handelt es sich um **"maker"**.
- Nur in Linux: Anstelle von [robot@ev3dev.local](mailto:robot@ev3dev.local), sollte man die IPv4-Adresse eingeben, welche auf dem Roboter unter **Wireless and Networks>All Network Connections>Wired>IPv4** zu finden ist. Also **ssh robot@IPv4**.

3. [Programmiersprache](https://github.com/ev3dev/ev3dev-lang-python)

- Hinweis zum Ausführen, immer über Run oder F5 gehen.
- Um sich mit dem Roboter zu verbinden, unter "ev3 device browser" auf "device not found" gehen und dann erst robot und dann die IPv4 Adresse eingeben.