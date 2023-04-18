import RPi.GPIO as GPIO
import time
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np

import RPi.GPIO as GPIO
# the pin numbers refer to the board connector not the chip
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)


PASSWORD_HASH = 'CHANGE TO A SHA256 HASH'

# Example to generate password Hash -  Example below is not the actual Password
# print(generate_password_hash('test','sha256'))



def checkGaragePassword(input_password):
    return check_password_hash(PASSWORD_HASH,input_password)
    

def triggerGarage():
    GPIO.output(7, GPIO.LOW)
    time.sleep(1)
    GPIO.output(7, GPIO.HIGH)
    print("Garage Triggered")
    time.sleep(12)


def checkGarageStatus():
    if GPIO.input(18) == GPIO.LOW:
        print("Garage is Open")
        return 'Open'
    else:
        print("Garage is Closed or Opening/Closing")
        return 'Question'


def garageCamera():
    camera = cv2.VideoCapture('http://192.168.68.118:4747/video')

    while True:
        success, frame = camera.read()  # read the camera frame

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        time.sleep(4)