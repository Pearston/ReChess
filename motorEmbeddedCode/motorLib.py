# This Motor library is used to create a motor, 
# access its specs, and control its movement.
from time import sleep
import RPi.GPIO as GPIO

DELAY = 0.0008/2

class Motor:

	# Constructor to set dir, step, clockwise, counter clockwise
	# If direction is 1, clockwise
	# If direction is 0, counter clockwise
	def __init__(self, dir_pin=None, step_pin=None, this_direction=1, this_mode=None, this_step_per_revolution=None,this_resolution='Full', this_scale=1):
		self.dir_pin = dir_pin
		self.step_pin = step_pin
		self.direction = this_direction
		self.mode = this_mode 
		self.resolution = this_resolution
		self.scale = this_scale
		self.step_per_revolution = this_step_per_revolution


	# This function is used to set up Raspberry pin to the motor specs.
	def initial_set_up(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.dir_pin, GPIO.OUT)
		GPIO.setup(self.step_pin, GPIO.OUT)
		GPIO.output(self.dir_pin, self.direction)
		GPIO.setup(self.mode, GPIO.OUT)

	# This function is used to set a motor in the clockwise direction.
	def set_clockwise(self):
		self.direction = 1 
		GPIO.output(self.dir_pin, self.direction)

	# This function is used to set a motor in the counter clockwise direction.
	def set_counter_clockwise(self):
		self.direction = 0
		GPIO.output(self.dir_pin, self.direction)

	# This function is used to set dir pin of the driver to a Pi pin
	def set_dir_pin(self, this_pin):
		self.dir_pin = this_pin
		GPIO.setup(self.dir_pin, GPIO.OUT)

	# This function is used to set step pin of the driver to a Pi pin
	def set_step_pin(self, this_pin):
		self.step_pin = this_pin
		GPIO.setup(self.step_pin, GPIO.OUT)


	# This function is used to set a microstepping resolution of the driver.
	# This driver has 6 mode: Full, Half, 1/4, 1/8, 1/16 and 1/32
	def set_resolution(self, key):
		resolution = {'Full': (0, 0, 0),
				'Half': (1, 0, 0),
				'1/4' : (0, 1, 0),
				'1/8' : (1, 1, 0),
				'1/16' : (0, 0, 1),
				'1/32' : (1, 0, 1)}
		self.resolution = key
		GPIO.output(self.mode, resolution[key])
		if key == 'Half':
			self.scale = 2
		elif key == '1/4':
			self.scale = 4 
		elif key == '1/8':
			self.scale = 8
		elif key == '1/16':
			self.scale = 16
		elif key == '1/32':
			self.scale = 32
		else:
			self.scale = 1

	# Motor moves 1 step based on the resolution
	def motor_steps(self, step_count):

		for x in range (step_count):

			GPIO.output(self.step_pin, GPIO.HIGH)
			sleep(DELAY)
			GPIO.output(self.step_pin, GPIO.LOW)
			sleep(DELAY)










