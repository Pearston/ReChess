import sys
from time import sleep
import RPi.GPIO as GPIO

class Button:

    def __init__(self, this_pin, this_delay):
        self.pin = this_pin
        self.start = False
        self.rearranging = False
        self.stop = False
        self.delay = this_delay
        GPIO.setmode(GPIO.BCM)

    def set_up(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def DebounceMain(this_button, start_queue, system_fsm):
    prev_temp = False
    prev = False
    curr = False
    curr_temp = False
    while True:
        prev_temp = curr_temp
        curr_temp = GPIO.input(this_button.pin)    #replace this with GPIO when possible
        prev = curr
        curr = curr_temp & prev_temp
        # print("prev_temp: " + str(prev_temp))
        # print("curr_temp: " + str(curr_temp))
        sleep(this_button.delay)
        if curr and not prev:
            print("BUTTON PRESSED")
            if system_fsm.not_start:
                system_fsm.running = True
                system_fsm.not_start = False
                system_fsm.piece_count = 0
                print("start system")

            
            elif system_fsm.running:
                system_fsm.running = False
                system_fsm.not_start = True
                print("end the system")
            start_queue.put(True)
            # # Advoid adding many values in start_queue
            while not start_queue.empty():
                sleep(1)
            print("START QUEUE JOINED")

            sleep(0.5)

            

