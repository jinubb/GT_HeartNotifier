#!/usr/bin/env python

import pigpio
import time

pinServo = 24

pi = pigpio.pi()

try:

    print "input pulse width from 500 to 2500"
    
    while 1:
    
        pw = int(input("pw = "))
        
        if( pw >= 500 and pw <= 2500 ):
            pi.set_servo_pulsewidth(pinServo, pw)
            time.sleep(0.1)
        else:
            print "pulse width have to be range in from 500 to 2500!"
            pw = int(input("pw = "))
            time.sleep(0.1)

except KeyboardInterrupt:
    print "\ntest code terminated."
    pi.stop()

'''
    3V3 . . 5V0
      2 . . 5V0
      3 . . GND
      4 . . 14
    GND . . 15
     17 . . 18  ------ output writeSync value to relay
     27 . . GND
     22 ._. 23  ------ generate signal for controlling servo
    3V3 . . 24  ------ connected to servo
     10 . . GND
      9 . . 25
     11 . . 8   
    GND . . 7
      0 . . 1
      5 . . GND
      6 . . 12
     13 . . GND
     19 . . 16
     26 . . 20
    GND . . 21
'''
