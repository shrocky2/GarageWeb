import time
from datetime import datetime
from flask import Flask, render_template, request

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set pin 16 as input and pull up to 3V via software pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set pin 18 as input and pull up to 3V via software pull-up resistor
GPIO.setup(7, GPIO.OUT) # output relay trigger 1
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT) # output relay trigger 2
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT) # output relay trigger 3
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT) # output relay trigger 4
GPIO.output(15, GPIO.HIGH)


# Change default password here. '12345678' is the default Password that Opens Garage Door.
passwd = '12345678'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if  request.method == 'POST':       
        name = request.form['garagecode']
        if name == passwd:
            # password correctly entered - toggle "button press"
            GPIO.output(7, GPIO.LOW)
            time.sleep(1)
            GPIO.output(7, GPIO.HIGH)
            time.sleep(2)
        else:
            if name == "":
                name = "[empty]"
            print("Garage Code Entered: " + name)

    if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        print("Garage is Opening/Closing")
        return app.send_static_file('Question.html')
    elif GPIO.input(16) == GPIO.LOW:
        print ("Garage is Closed")
        return app.send_static_file('Closed.html')
    elif GPIO.input(18) == GPIO.LOW:
        print ("Garage is Open")
        return app.send_static_file('Open.html')

@app.route('/stylesheet.css')
def stylesheet():
        return app.send_static_file('stylesheet.css')

@app.route('/log')
def logfile():
        return app.send_static_file('log.txt')

@app.route('/images/<picture>')
def images(picture):
        return app.send_static_file('images/' + picture)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
