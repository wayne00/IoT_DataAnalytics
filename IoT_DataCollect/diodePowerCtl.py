#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import time

channel = 17

def setDiodeState(temp,desire_new_threshold):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    state = 0
    print("********setDiodeState:*******")
    print("The temp %f is and desire_new_threshold is %f " % (temp,desire_new_threshold))  
    # GPIO.setup(channel, GPIO.OUT)
    # desire "on"
    if (temp>desire_new_threshold):
        state = 1
        GPIO.output(channel, GPIO.HIGH)
    # desire "off"
    else:
        state = 0
        GPIO.output(channel, GPIO.LOW)
    time.sleep(2)
    # desire == "on"
    if (state == 1):
        return "ON"
    # desire == "off"
    elif (state == 0):
        return "OFF"
    else:
        return "error"


def setDiodeDoor(StrState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    state = 0
    print("********setDiodeState:*******")
    # 设置发光二极管状态为开 "on"
    if (StrState == "ON"):
       	print ("================================on==================================")
	    state = 1
        GPIO.output(channel, state)
    # 设置发光二极管状态为关 "off"
    else:
	    print("================================off==================================")
        state = 0
        GPIO.output(channel, state)

    # desire == "on"
    if (state == 1):
        return "ON"
    # desire == "off"
    elif (state == 0):
        return "OFF"
    else:
        return "error"


if __name__ == '__main__':
    setDiodeDoor(sys.argv[1])
