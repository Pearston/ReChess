from time import sleep
import RPi.GPIO as GPIO

DIR = 19 		# Direction GPIO Pin
STEP = 26		# Step GPIO
CW = 1 			# Clockwise Rotation
CCW = 0 		# Counterclockwise Rotation
SPR = 1200 		# Steps per Revolution

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
				'Half': (1, 0, 0),
				'1/4' : (0, 1, 0),
				'1/8' : (1, 1, 0),
				'1/16' : (0, 0, 1),
				'1/32' : (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['Half'])
step_count = SPR*2
# step_count = SPR
delay = 0.0008/2


for x in range (step_count):
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	sleep(delay)


sleep(0.5)
GPIO.output(DIR, CCW)

for x in range (step_count):
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	sleep(delay)