import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './motorEmbeddedCode')
sys.path.insert(1, './imageProcessingCode')

from abstractionMaker import *
import piece
import cameraDriver
import math
import corexyLib
import RPi.GPIO as GPIO
import motorLib
import movement
import eMagnetLib
from rearrangement import *
from time import sleep
import gc

def generate_input():
    
    myCamera = cameraDriver.ReChessCamera()
    myCamera.takeAPicture()
    current_board, piece_list = getAbstraction()
    
    # while(len(piece_list) != 32):
        
    #     print("hi")
    #     myCamera.takeAPicture()
    #     current_board, piece_list = getAbstraction()

    myCamera.closeCamera()

    state_board = generate_state_board()
    current_board = [list(row) for row in current_board]
    return current_board, piece_list, state_board

# setting up camera
# myCamera = cameraDriver.ReChessCamera()

# take a picture of the camera
# myCamera.takeAPicture()

# Create a core xy
corexy = corexyLib.CoreXY(20, 'Half', motorLib.Motor(20, 21, 1, (14, 15, 18), 400, 'Half'), motorLib.Motor(19, 26, 1, (14, 15, 18), 400, 'Half'), eMagnetLib.EMagnet(5),0, 0)
# Set up the corexy
corexy.set_up()


# using image processing to create the input current_board
current_board, piece_list, state_board = generate_input()

print("Current board:")
for row in current_board:
    print(row)

for this_piece in piece_list:
    print(str(this_piece))


movementQueue = []
piece_dictionary = {}

try:
    board_rearranged, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

    while board_rearranged == False:
        print("Board is not rearranged.")
        print("Piece to arrange:")

        print(piece_to_arrange)
        rearrange_piece(piece_to_arrange, corexy, movementQueue, piece_dictionary, current_board)

        for this_move in movementQueue:
            print(this_move)
            
            corexy.make_a_move(this_move)
            # print("done")
            # sleep(5)

        sleep(0.5)
        # corexy.move_to(0,0)

        current_board, piece_list, state_board = generate_input()

        movementQueue = []
        piece_dictionary = {}

        # clean up memory
        gc.collect()

        board_rearranged, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

    if (board_rearranged):
        print("Board is rearranged")
        corexy.move_to(0,0)

except Exception as e:
    print(e)
    


# # Create a piece
# # name, row =None, col=None, x_coor=None, y_coor=None, dest_row=None, dest_col=None, dest_occupied=None):
# this_piece = piece.Piece("BP", 5, 6, None, None, 2, 4, False)

# # corexy.move_up(2500)
# # corexy.move_down(2500)
# movementQueue = []

# rearrange_piece(this_piece, corexy, movementQueue)

# corexy2 = corexyLib.CoreXY(20, 'Half', motorLib.Motor(20, 21, 1, (14, 15, 18), 400, 'Half'), motorLib.Motor(19, 26, 1, (14, 15, 18), 400, 'Half'), 0, 0)
# # Set up the corexy
# corexy2.set_up()

# # x_coor, y_coor = cal_destination_coor(this_piece.row, this_piece.col)
# # corexy2.move_to(x_coor,y_coor)
# # corexy2.move_to(0, 0)

# for this_move in movementQueue:
#     print(this_move)
#     corexy2.make_a_move(this_move)

# corexy2.move_to(0,0)

# while True:
#     if GPIO.input(23) == GPIO.HIGH:
#         print("Button was pushed")









