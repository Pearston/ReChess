import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)


XBUMP = 3
YBUMP = 4
GPIO.setup(XBUMP,GPIO.IN)
GPIO.setup(YBUMP,GPIO.IN)

while True:
    sleep(1)
    if not GPIO.input(3):
        print("bump X is pressed")
    if not GPIO.input(4):
        print("bump Y is pressed")



    