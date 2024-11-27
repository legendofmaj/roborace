#!/usr/bin/env python3

from ev3dev2.sound import Sound
import time

speaker = Sound()
volume = 100

def firstSoundFile():
    speaker.play_file('/home/robot/Roborace/miscellaneous/soundFiles/Edited/Audio1.wav', volume=volume, play_type=0)

def secondSoundFile():
    speaker.play_file('/home/robot/Roborace/miscellaneous/soundFiles/Edited/Audio2.wav', volume=volume, play_type=0)

#example usage
def main():
    firstSoundFile()
    time.sleep(1)
    secondSoundFile()

    if __name__=="__main__":
        main()

def startingFanfare():
    speaker.play_song([('C4',500), ('F4',250), ('C4',250)])#to be played before starting to navigate thru course

def finishFanfare():
    speaker.play_song([('C4', 400), ('E4', 400), ('G4', 400), ('B4', 400), ('G4', 400), ('B4', 650)])#to be played after finishing course

def main():
    startingFanfare()
    time.sleep(1)
    finishFanfare()

    if __name__=="__main__":
        main()