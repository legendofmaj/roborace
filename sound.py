#!/usr/bin/env python3

from ev3dev2.sound import Sound

speaker = Sound()
volume = 100

def firstSoundFile():
    speaker.play_file('/home/robot/Roborace/miscellaneous/soundFiles/Audio1.wav', volume=volume, play_type=0)

def firstSoundTone():
    speaker.play_tone(220, 1, 0.1, volume=volume, play_type=0)

def secondSoundFile():
    speaker.play_file('/home/robot/Roborace/miscellaneous/soundFiles/Audio2.wav', volume=volume, play_type=0)

def secondSoundTone():
    speaker.play_tone(180, 1, 0.1, volume=volume, play_type=0)

def thirdSoundTone():
    speaker.play_tone(140, 3, 2, volume=volume, play_type=0)

def main():
    firstSoundFile()
    secondSoundFile()

if __name__=="__main__":
    main()
