#!/usr/bin/env python3

from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import array
import math
import time

#from ast import Return
#from cmath import e
#from datetime import time
#from email.errors import NonASCIILocalPartDefect
#from glob import glob
#from lib2to3.pgen2.token import CIRCUMFLEX
#from pickletools import float8
from threading import Thread, Event
from time import sleep
#from tkinter import EventType
#from tracemalloc import start
#from turtle import circle, st



diststart=17
circleAngle=0.0
distarryx=(list(range(0,360)))
distarry=(list(range(0,360)))
mind=1000000
minphi=1000000
mindavg=1000000
minphiavg=1000000

gyroSensor = GyroSensor(INPUT_2)
ultraSoundSensor = UltrasonicSensor(INPUT_3)
tankDrive = MoveTank(OUTPUT_C, OUTPUT_B)

# def task(event: Event, id: int) -> None:
#     #print(f'Thread {id} started. Waiting for the signal...')
#     event.wait()
#     print(f'Received signal. The thread {id} was completed.')


def read_distv(event: Event, id: int) -> None:
    print("thread read_distv started")
    global diststart
    count_read_distv = 0
    while True:
        global dist 
        dist = diststart #ultraSoundSensor.distance_centimeters
        count_read_distv+=1
        sleep(0.05)
        print("Thread read_distv",count_read_distv)

def readCircleAnglev(angstart: float,incr: float, event: Event)->None:
    global circleAngle 
    circleAngle = angstart
    count_read_distc=0
    while not event.isSet():
        circleAngle += incr
        if circleAngle>=360.0:
            circleAngle=0.0
        if circleAngle<0:
            circleAngle=359.0
        sleep(0.05)
        count_read_distc+=1
        print("Thread readCircleAnglev",count_read_distc,circleAngle)

# turning left
def relturnv(degrees, speed):
    global circleAngle
    cpos = circleAngle
    target = cpos + degrees
    print("relturnv.target:",target)
    tolerance=5
    if (target<360):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle < target-tolerance:
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            print("relturnv.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnv.Done1")
    else:
        npos=0
        while ((circleAngle+npos<target-tolerance)):
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            if circleAngle<cpos:
                npos=360
            print("relturnv.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnv.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnv.Done3")


# swiping left
def relswipel(degrees, speed):
    global distarry
    global circleAngle
    global mind
    global minphi
    cpos = circleAngle
    target = cpos + degrees
    print("relturnv.target:",target)
    tolerance=5
    if (target<360):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle < target-tolerance:
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            print("relturnv.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(circleAngle)]
            print("distance:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=circleAngle
        print("relturnv.Done1")
    else:
        npos=0
        while ((circleAngle+npos<target-tolerance)):
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            if circleAngle<cpos:
                npos=360
            print("relturnv.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(circleAngle)]
            print("distance:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=circleAngle
        print("relturnv.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnv.Done3")
    print("minphi:",minphi,"mind:",mind)


# turntoxl
def turntoxl(degrees, speed):
    global circleAngle
    cpos = circleAngle
    target = degrees
    print("turntoxl.target:",target)
    tolerance=5
    if (target>=cpos):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle < target-tolerance:
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            print("turntoxl.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
        print("turntoxl.Done1")
    else:
        npos=360
        while ((circleAngle-npos<target-tolerance)):
            tankDrive.on(SpeedPercent(speed), SpeedPercent(-speed))
            sleep(0.1)
            if cpos-circleAngle>0:
                npos=0
            print("turntoxl.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
        print("turntoxl.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("turntoxl.Done3")



# turning right
def relturnr(degrees, speed):
    global circleAngle
    cpos = circleAngle
    target = cpos - degrees
    print("relturnr.target:",target)
    tolerance=5
    if (target>0):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle > target+tolerance:
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            print("relturnr.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnr.Done1")
    else:
        npos=0
        while ((circleAngle-npos>target+tolerance)):
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            if cpos-circleAngle<0:
                npos=360
            print("relturnr.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnr.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnr.Done3")

#swiping right
def relswiper(degrees, speed):
    global distarry
    global circleAngle
    global mind
    global minphi

    cpos = circleAngle
    target = cpos - degrees
    print("relswiper.target:",target)
    tolerance=5
    if (target>0):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle > target+tolerance:
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            print("relswiper.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(circleAngle)]
            print("relswiper.distance1:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=circleAngle
        print("relswiper.Done1")
    else:
        npos=0
        while ((circleAngle-npos>target+tolerance)):
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            if cpos-circleAngle<0:
                npos=360
            print("relswiper.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
            dphi=distarry[int(circleAngle)]
            print("relswiper.distance2:",dphi)
            if dphi<mind:
                mind=dphi
                minphi=circleAngle
        print("relswiper.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("relswiper.Done3")
    print("minphi:",minphi,"mind:",mind)



# turning right
def turntoxr(degrees, speed):
    global circleAngle
    cpos = circleAngle
    target = degrees
    print("relturnr.target:",target)
    tolerance=5
    if (target<cpos):
        #startAngle =  getRelAnglev(cpos) #getRelAngle(cpos) # Sollte nahe 0 sein, wenn Roboter nicht in Drehung ist
        #while abs(getRelAnglev(cpos)) < max(degrees, 10): # minimale Drehung 10� 
        while circleAngle > target+tolerance:
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            print("relturnr.circleAngle1:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnr.Done1")
    else:
        npos=360
        while ((circleAngle+npos>target+tolerance)):
            tankDrive.on(SpeedPercent(-speed), SpeedPercent(speed))
            sleep(0.1)
            if cpos-circleAngle<0:
                npos=0
            print("relturnr.circleAngle2:", circleAngle) #, (getRelAnglev(cpos)))
        print("relturnr.Done2")
    tankDrive.on(SpeedPercent(0), SpeedPercent(0))
    print("relturnr.Done3")

# swipelr
def swipelr(spos):
    global distarry
    global circleAngle
    global mind
    global minphi
    global mindavg
    global minphiavg
    # event = Event()
    print("swiping left")
    # circleAngleThread = Thread(target = readCircleAnglev, args=(spos,1.0, event)) #dreht links
    # print('Starting thread...')
    # circleAngleThread.start()

    relswipel(45,10.0)

    sleep(1)
    # event.set()
    # circleAngleThread.join()
    # event.clear()

    lmind=mind
    lphi=minphi

    print("swiping right")
    # circleAngleThread = Thread(target = readCircleAnglev, args=(spos+20,-1.0, event)) #dreht rechts
    # print('Starting thread...')
    # circleAngleThread.start()

    relswiper(45,10.0)
    sleep(1)
    # event.set()
    # circleAngleThread.join()
    # event.clear()
    mindavg=(mind+lmind)/2
    minphiavg=(minphi+lphi)/2
    print("mind l:",lmind,"mind r:",mind,"mind Avg:",mindavg)
    print("minphi l:",lphi,"mind r:",minphi,"mind Avg:",minphiavg)


def getRelAnglev(spos):
    global circleAngle
    temp = circleAngle - spos
    return temp

def read_dist():
    while True:
        global dist 
        dist = ultraSoundSensor.distance_centimeters
        time.sleep(0.05)

def readCircleAngle():
    global circleAngle
    global Angle
    while True:
        circleAngle = gyroSensor.circle_angle()
        Angle = gyroSensor.angle
        time.sleep(0.12)
        #print(circleAngle)

def startThreads():
    distThread = Thread(target= read_dist)
    distThread.start()
    # buttonThread =Thread(target = readButton)
    # buttonThread.daemon = True
    # buttonThread.start()
    # colorThread = Thread(target = readColor)
    # colorThread.start()
    #angleThread = threading.Thread(target = readAngle)
    #angleThread.start()
    circleAngleThread = Thread(target = readCircleAngle)#, args=(stop_event))
    circleAngleThread.start()

def main() -> None:
    global circleAngle

    startThreads()


###    event = Event()

    #distThread = Thread(target=read_distv, args=(event, 1))

###    print("turning left")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(355,1.0, event)) #dreht links
###    #t1 = Thread(target=task, args=(event, 1))
###    #t2 = Thread(target=task, args=(event, 2))
###
###    #t1.start()
###    #t2.start()
###    #distThread.start()
###    print('Starting thread...')
###    circleAngleThread.start()
###
###    starttime = time().second
###    relturnv(20,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()
###    print("turning left again")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(305,1.0, event)) #dreht links
###    print('Starting thread...')
###    circleAngleThread.start()
###    relturnv(20,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()

###    print("turning right")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(10,-1.0, event)) #dreht rechts
###    print('Starting thread...')
###    circleAngleThread.start()
###    relturnr(20,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()

###    print("turning right again")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(45,-1.0, event)) #dreht rechts
###    print('Starting thread...')
###    circleAngleThread.start()
###    relturnr(20,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()

###    print("turning left absolut")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(350,1.0, event)) #dreht links
###    print('Starting thread...')
###    circleAngleThread.start()
###    starttime = time().second
###    turntoxl(15,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()

###    print("turning left absolut again")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(5,1.0, event)) #dreht links
###    print('Starting thread...')
###    circleAngleThread.start()
###    turntoxl(25,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()
###

###    print("turning right absolute")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(10,-1.0, event)) #dreht rechts
###    print('Starting thread...')
###    circleAngleThread.start()
###    turntoxr(350,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()
###
###    print("turning right absolute again")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(45,-1.0, event)) #dreht rechts
###    print('Starting thread...')
###    circleAngleThread.start()
###    turntoxr(20,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()

    global distarryx
    global distarry
    global mindavg
    global minphiavg

    for i in distarryx:
        distarry[i]= 20+15.0*(1-(math.sin(i*math.pi/360)*math.sin(i*math.pi/360)))


###    print("swiping left")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(170,1.0, event)) #dreht links
###    print('Starting thread...')
###    circleAngleThread.start()
###
###    starttime = time().second
###    relswipel(25,1.0)
###
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()
###
###    lmind=mind
###    lphi=minphi
###
###    print("swiping right")
###    circleAngleThread = Thread(target = readCircleAnglev, args=(190,-1.0, event)) #dreht rechts
###    print('Starting thread...')
###    circleAngleThread.start()
###
###    starttime = time().second
###    relswiper(25,1.0)
###    sleep(1)
###    event.set()
###    circleAngleThread.join()
###    event.clear()
    swipelr(170)
    print("------------ mind Avg:",mindavg)
    print("------------ minphi Avg:",minphiavg)

    # event = Event()
    print("turning left absolut")
    # circleAngleThread = Thread(target = readCircleAnglev, args=(170,1.0, event)) #dreht links
    # print('Starting thread...')
    # circleAngleThread.start()
    turntoxl(minphiavg,10.0)
    sleep(1)
    # event.set()
    # circleAngleThread.join()
    # event.clear()




if __name__ == '__main__':
    main()