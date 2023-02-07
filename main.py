import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './motorEmbeddedCode')
sys.path.insert(1, './imageProcessingCode')

import RPi.GPIO as GPIO
import button
import corexyLib
import fsm

from rearrangement import *
from button import *
from fsm import *
from time import sleep
from threading import Thread
from queue import Queue

def main():

    # Create a button for the system
    this_button = button.Button(23, .010)
    this_button.set_up()
    
    # Create corexy 
    corexy = corexyLib.CoreXY(20, 'Half', 
        motorLib.Motor(20, 21, 1, (14, 15, 18), 400, 'Half'), 
		motorLib.Motor(19, 26, 1, (14, 15, 18), 400, 'Half'), 
		eMagnetLib.EMagnet(5),0, 0)
    corexy.set_up()

    # Create FSM for the system.
    # The FSM includes three states: not_start, running, end
    system_fsm = fsm.FSM() 

    # Create a queue to store the button press.
    start_queue = Queue()

    # Create thread that waits for the Start Button
    button_thread = Thread(target=DebounceMain, args=(this_button, start_queue, system_fsm))

    button_thread.start()
    
    while True:
    
        # If start_queue is not empty, the start button is pressed to start
        # rearranging the pieces.
        if not start_queue.empty():

            # Check if button_thread did put extra value to start_queue
            # If button_thread added many values in start_queue, 
            # we filtered them out.
            while not start_queue.empty():
                start_queue.get()
            
            if system_fsm.running:
                print("start rearrange")
                start_rearrange(corexy, system_fsm)
        
        #add delay so other threads get attention
        sleep(.02)

if __name__ == "__main__":
    main()