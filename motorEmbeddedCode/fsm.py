import sys

# This is the Finite State Machine class.
class FSM():

    def __init__(self):
        self.not_start = True
        self.running = False
        self.piece_count = 0

def FSM_main(system_fsm, start_queue):
    while True:
        if not start_queue.empty():

            # Check if button_thread did put extra value to start_queue
            # If button_thread added many values in start_queue, 
            # we filtered them out.
            while not start_queue.empty():
                start_queue.get()
            
            # The button is pressed. If the system is not started,
            # we start the system and update it to running state.
            if system_fsm.not_start:
                system_fsm.running = True
                system_fsm.not_start = False
                print("start system")

            
            elif system_fsm.running:
                system_fsm.running = False
                system_fsm.not_start = True
                print("end the system")




