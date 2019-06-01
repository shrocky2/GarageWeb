import time
from datetime import datetime
from flask import Flask, render_template, request

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
             print("Garage is Opening/Closing")
             return app.send_static_file('Question.html')
        else:  
             if GPIO.input(16) == GPIO.LOW:
                   print ("Garage is Closed")
                   return app.send_static_file('Closed.html')
             if GPIO.input(18) == GPIO.LOW:
                   print ("Garage is Open")
                   return app.send_static_file('Open.html')


@app.route('/Garage', methods=['GET', 'POST'])
def Garage():
        name = request.form['garagecode']
        if name == '12345678':  # 12345678 is the Password that Opens Garage Door (Code if Password is Correct)
                GPIO.output(7, GPIO.LOW)
                time.sleep(1)
                GPIO.output(7, GPIO.HIGH)
                time.sleep(2)

                if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
                  print("Garage is Opening/Closing")
                  return app.send_static_file('Question.html')
                else:
                  if GPIO.input(16) == GPIO.LOW:
                        print ("Garage is Closed")
                        return app.send_static_file('Closed.html')
                  if GPIO.input(18) == GPIO.LOW:
                        print ("Garage is Open")
                        return app.send_static_file('Open.html')

        if name != '12345678':  # 12345678 is the Password that Opens Garage Door (Code if Password is Incorrect)
                if name == "":
                        name = "NULL"
                print("Garage Code Entered: " + name)
                if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
                  print("Garage is Opening/Closing")
                  return app.send_static_file('Question.html')
                else:
                  if GPIO.input(16) == GPIO.LOW:
                        print ("Garage is Closed")
                        return app.send_static_file('Closed.html')
                  if GPIO.input(18) == GPIO.LOW:
                        print ("Garage is Open")
                        return app.send_static_file('Open.html')

@app.route('/stylesheet.css')
def stylesheet():
        return app.send_static_file('stylesheet.css')

@app.route('/Log')
def logfile():
        return app.send_static_file('log.txt')

@app.route('/images/<picture>')
def images(picture):
        return app.send_static_file('images/' + picture)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
