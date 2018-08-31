import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import subprocess
import logging
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

logging.basicConfig(filename="rasberryLogfile.log", level=logging.DEBUG)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   26 : {'name' : 'LED 1', 'state' : GPIO.LOW, 'css' : 'button1'},
   20 : {'name' : 'LED 3', 'state' : GPIO.LOW, 'css' : 'button3'},
   21 : {'name' : 'LED 4', 'state' : GPIO.LOW, 'css' : 'button4'},
   16 : {'name' : 'Light', 'state' : GPIO.LOW, 'css' : 'button5'},
   19 : {'name' : 'LED 2', 'state' : GPIO.LOW, 'css' : 'button2'}
   }



# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins,
    'soundFile' : 'static/bleep_01.wav'

      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins,
      'soundFile' : '../../static/bleep_01.wav'
   }

   return render_template('main.html', **templateData)

@app.route("/playSound")
def playSound():
    logging.debug("playing sound")
    subprocess.call("sudo aplay bleep_01.wav", shell=True)
    logging.debug("played sound")
    templateData = {
        'pins' : pins,
        'soundFile' : '../static/bleep_01.wav'
    }
    return render_template('main.html', **templateData)

@app.route("/bleep_01.wav")
def playSound1():
    templateData = {
        'pins' : pins
    }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)