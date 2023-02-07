from time import sleep
import RPi.GPIO as GPIO


# This class presents the electro magnet class
class EMagnet:


	# Constructor to defind an electro magnet.
	# The electro magnet is off by default
	def __init__ (self, thisPin=None, thisIsOn = False):

		self.pin = thisPin
		self.isOn = thisIsOn

	# This function is used to set up Raspberry pin to the electro magnet
	# pin.
	def initial_set_up(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)


	# This function is used to turn on the electro magnet.
	def turn_on(self):
		self.isOn = True
		GPIO.output(self.pin, GPIO.HIGH)


	# This function is used to turn off the electro magnet.
	def turn_off(self):
		self.isOn = False
		GPIO.output(self.pin, GPIO.LOW)






