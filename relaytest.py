print(" Control + C to exit Program")

import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)     # sets the pin input/output setting to OUT
GPIO.output(7, GPIO.HIGH)   # sets the pin output to high
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)

try:
  GPIO.output(7, GPIO.LOW)   # turns the first relay switch ON
  time.sleep(.5)             # pauses system for 1/2 second
  GPIO.output(7, GPIO.HIGH)  # turns the first relay switch OFF

except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches
