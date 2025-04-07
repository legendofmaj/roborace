#!/usr/bin/env python3

from ev3dev2.sound import Sound

speaker = Sound()
volume = 100

def firstSound():
    speaker.play_file('miscellaneous/soundFiles/Audio1.wav', volume, play_type=0)

def secondSound():
    speaker.play_file('miscellaneous/soundFiles/Audio2.wav', volume, play_type=0)

def main():
    speaker.play_tone(440, 2, 2, play_type=0)
    firstSound()
    secondSound()

if __name__=="__main__":
    main()
