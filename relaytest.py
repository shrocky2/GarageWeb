print " Control + C to exit Program"

import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)     # sets the pin input/output setting to OUT
GPIO.output(7, GPIO.HIGH)   # sets the pin output to high
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)

try:
  while 1 >=0:
    GPIO.output(7, GPIO.LOW)   # turns the first relay switch ON
    time.sleep(.5)             # pauses system for 1/2 second
    GPIO.output(7, GPIO.HIGH)  # turns the first relay switch OFF
    GPIO.output(11, GPIO.LOW)  # turns the second relay switch ON
    time.sleep(.5)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    time.sleep(.5)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(15, GPIO.LOW)
    time.sleep(.5)
    GPIO.output(15, GPIO.HIGH)
    time.sleep(.5)

except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches
