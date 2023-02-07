#import Servomotor
from socket import *
from time import ctime
import time
import struct
import base64
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './motorEmbeddedCode')
sys.path.insert(1, './imageProcessingCode')

from abstractionMaker import *
import piece
import math
import corexyLib
import RPi.GPIO as GPIO
import motorLib
import movement
import eMagnetLib
import cameraDriver
from rearrangement import *
from time import sleep
import gc

SQUARE_SIDE = 50.8
# Create a core xy
corexy = corexyLib.CoreXY(20, 'Half', motorLib.Motor(20, 21, 1, (14, 15, 18), 400, 'Half'), motorLib.Motor(19, 26, 1, (14, 15, 18), 400, 'Half'), eMagnetLib.EMagnet(5),0, 0)
# Set up the corexy
corexy.set_up()
current_board = []

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

# using image processing to create the input current_board
current_board, piece_list, state_board = generate_input()
print("Current board:")
for row in current_board:
    print(row)

for this_piece in piece_list:
    print(str(this_piece))

def rearrange(current_board, piece_list, state_board):
    movementQueue = []
    piece_dictionary = {}
    try:
    
        board_rearranged, min_distance, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)
        # this_piece = piece.Piece("BP", 5, 7, 279.4, 330.2, 2, 4, False)

        while board_rearranged == False :
            print("Booard is not rearranged.")
            print("Piece to arrange:")

            print(piece_to_arrange)
            rearrange_piece(piece_to_arrange, corexy, movementQueue, piece_dictionary, current_board)

            for this_move in movementQueue:
                print(this_move)
                
                corexy.make_a_move(this_move)
                # print("done")
                # sleep(5)

            
            sleep(5)
            # corexy.move_to(0,0)

            current_board, piece_list, state_board = generate_input()
            movementQueue = []
            piece_dictionary = {}

            # clean up memory
            gc.collect()

            board_rearranged, min_distance, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

        if (board_rearranged):
            print("Board is rearranged")
            corexy.move_to(0,0)

    except Exception as e:
        print(e)





#import RPi.GPIO as GPIO

#Servomotor.setup()

# for other python-python
# ctrCmd = ['Up','Down']
chessboard = [['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'WK', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA'],
                ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA']]



# for phone
ctrCmd = ['Up', 'Rearrange', 'Move', 'Picture', 'Abstraction']
#ctrCmd = [b'1',b'2']


#NI LAB
HOST =  "172.25.129.62"
#home
#HOST = "172.26.69.112"
#HOST = "172.25.142.78"
PORT = 9077
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)


while True:
    print('Waiting for connection')
    tcpCliSock,addr = tcpSerSock.accept()
    print('...connected from :' + str(addr))

    try:
        while True:
            data = ''
            data = tcpCliSock.recv(BUFSIZE)
            
            # gets rid of java stuff at beginning of command
            command = data[2:len(data)].decode()

            print(command)
    
            if not command:
                print(str(data))
                break
            if command == ctrCmd[0]:
                #Servomotor.ServoUp()
                print ('SERVER - Increase: ')
            if command == ctrCmd[1]:
                #Servomotor.ServoDown()
                print ('SERVER - Rearrange: ')
                rearrange(current_board, piece_list, state_board)
            if command == ctrCmd[2]:
                print ('SERVER - Move Piece: ')
                pieceData = tcpCliSock.recv(BUFSIZE)
                pieceString = pieceData[2:len(pieceData)].decode()
                startPiece, endPiece = pieceString.split(',')
                print(startPiece)
                print(endPiece)

            if command ==  ctrCmd[3]:
                print('SERVER - Picture: ')
                with open("chessboard.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
  
                print("hi")
                tcpCliSock.send('\n'.encode())
                tcpCliSock.send(encoded_string)
                tcpCliSock.send('\n'.encode())
                tcpCliSock.send('<END>'.encode())
                tcpCliSock.send('\n'.encode())
            
            if command == ctrCmd[4]:
                print('SERVER - Abstraction: ')

                for row in range(len(chessboard)):
                    for col in range(len(chessboard)):
                        val = chessboard[row][col]
                        tcpCliSock.send(val.encode())
                        tcpCliSock.send('\n'.encode())
                
                # tcpCliSock.send('<END>'.encode())
                # tcpCliSock.send('\n'.encode())




    except KeyboardInterrupt:
        # Servomotor.close()
        # GPIO.cleanup()
        break
tcpSerSock.close()