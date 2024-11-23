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
