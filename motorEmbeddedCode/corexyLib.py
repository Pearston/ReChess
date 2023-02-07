# The CoreXY library implements the CoreXY system and its movement.
# The library uses the motorLib to access the two motors.
import motorLib
import eMagnetLib
import RPi.GPIO as GPIO
from time import sleep
import math
import movement

DELAY = 0.0008/2
DELAY2 = 0.0008

class CoreXY:

	# The constructor to create a corexy includes: the belt pitch, the pulley tooth
	# the resolution (microstepping) of the two motors, motorA, and motorB
	def __init__(self, this_step_per_mm, this_resolution, this_motorA= motorLib.Motor(), this_motorB= motorLib.Motor(), \
					this_eMagnet = eMagnetLib.EMagnet(), this_current_x=0, this_current_y=0):
		self.step_per_mm = this_step_per_mm
		self.resolution = this_resolution
		self.motorA = this_motorA
		self.motorB = this_motorB
		self.eMagnet = this_eMagnet
		self.current_x = this_current_x
		self.current_y = this_current_y
		GPIO.setmode(GPIO.BCM)

	# The function sets up the two motors
	def set_up(self):
		self.motorA.initial_set_up()
		self.motorB.initial_set_up()
		self.eMagnet.initial_set_up()

	# The function turns on the electro magnet of this corexy.
	def turn_eMagnet_on(self):
		sleep(DELAY2)
		self.eMagnet.turn_on()
		sleep(DELAY2)

	# The function turns off the electro magnet of this corexy.
	def turn_eMagnet_off(self):
		# sleep(DELAY2)
		self.eMagnet.turn_off()
		sleep(DELAY2)

	# The function is used to set resolution of the two motors based on the resolution
	# of the coreXY.
	def set_motors_resolution(self, motorA, motorB):
		motorA.setresolution(self.resolution)
		motorB.setresolution(self.resolution)
		


	# This function is used to step two motors at the same time.
	# Each motor steps one micro step only. 
	def step_motors(self):
		GPIO.output(self.motorA.step_pin, GPIO.HIGH)
		GPIO.output(self.motorB.step_pin, GPIO.HIGH)
		sleep(DELAY)
		GPIO.output(self.motorA.step_pin, GPIO.LOW)
		GPIO.output(self.motorB.step_pin, GPIO.LOW)
		sleep(DELAY)

	# The function moves the carriage up with 1 micro step from both motors.
	# The motors rotate in the opposite directions. 
	# A can be clockwise and B can be counter clockwise
	def move_up(self, step_count):
		self.motorA.set_clockwise()
		self.motorB.set_counter_clockwise()
		print("move up " + str(step_count))

		for x in range (step_count):
			self.step_motors()


	# The function moves the carriage down with 1 step from both motors.
	# The motors rotate in the opposite directions. 
	# A can be clockwise and B can be counter clockwise
	def move_down(self, step_count):
		self.motorA.set_counter_clockwise()
		self.motorB.set_clockwise()
		print("move down " + str(step_count))

		for x in range (step_count):
			self.step_motors()


	# The function moves the carriage to the right with 1 step from both motors.
	# The motors rotate in the same directions. 
	# A can be clockwise and B can be clockwise.
	def move_right(self, step_count):
		self.motorA.set_clockwise()
		self.motorB.set_clockwise()
		print("move right " + str(step_count))
		for x in range (step_count):
			self.step_motors()


	# The function moves the carriage to the left with 1 step from both motors.
	# The motors rotate in the same directions. 
	# A is counter clockwise and B is counter clockwise.
	def move_left(self, step_count):
		self.motorA.set_counter_clockwise()
		self.motorB.set_counter_clockwise()
		print("move left " + str(step_count))
		for x in range (step_count):
			self.step_motors()

	# This function moves the carriage to a new coordinate (x,y)
	# horizontally and vertically.
	def move_to(self, new_x_coor, new_y_coor):

		print("Cariage move from (" + str(self.current_x) + ", " + str(self.current_y) + ") to (" + str(new_x_coor) + ", " + str(new_y_coor) + ")")
		delta_x = new_x_coor-self.current_x 	# in mm
		delta_y = new_y_coor-self.current_y		# in mm

		steps_in_x = math.floor(self.step_per_mm * abs(delta_x))
		steps_in_y = math.floor(self.step_per_mm * abs(delta_y))

		if delta_x < 0:
			self.move_left(steps_in_x)
		else:
			self.move_right(steps_in_x)
		
		if delta_y < 0:
			self.move_down(steps_in_y)
		else:
			self.move_up(steps_in_y)
		
		self.current_x = new_x_coor
		self.current_y = new_y_coor
	

	def make_a_move(self, this_move):

		# Check if this move is a step movement
		if this_move.is_step:

			if this_move.direction == "left":
				self.move_left(int(this_move.step_count))
			elif this_move.direction == "right":
				self.move_right(int(this_move.step_count))
			elif this_move.direction == "up":
				self.move_up(int(this_move.step_count))
			else:
				self.move_down(int(this_move.step_count))
			
			self.current_x = this_move.dest_x
			self.current_y = this_move.dest_y

		# If this move is to control electro magnet
		else:

			if this_move.eMagnet_on:
				self.turn_eMagnet_on()
			else:
				self.turn_eMagnet_off()

		










