import sys
sys.path.insert(1, './imageProcessingCode')
import piece
import math
import corexyLib
import motorLib
import movement
import gc
import cameraDriver
import eMagnetLib
import fsm

from abstractionMaker import *
from time import sleep


# R is Rook, N is Knight, B is Bishop, Q is Queen, K is King, P is Pawn
# Dictionary stores the right squares of black pieces. This acts like the
# constants for all algorithm.
BLACK_SQUARE = { "BR1" : [1,1], "BN1" : [1,2], "BB1": [1,3], "BQ1" : [1,5],
			"BK1": [1,4], "BB2" : [1,6], "BN2": [1,7], "BR2": [1,8], 
			"BP1": [2,1], "BP2": [2,2], "BP3": [2,3], "BP4": [2,4],
			"BP5": [2,5], "BP6": [2,6], "BP7": [2,7], "BP8": [2,8]}

# Declare the dictionaries that holds the destination coordinates (mm) of 
# black pieces
BLACK_COOR = { "BR1" : [0,0], "BN1" : [0,0], "BB1": [0,0], "BQ1" : [0,0],
			"BK1": [0,0], "BB2" : [0,0], "BN2": [0,0], "BR2": [0,0], 
			"BP1": [0,0], "BP2": [0,0], "BP3": [0,0], "BP4": [0,0],
			"BP5": [0,0], "BP6": [0,0], "BP7": [0,0], "BP8": [0,0]}

# print(BLACK_SQUARE["BR1"])

# Dictionary stores the right squares of white pieces. This acts like the
# constants for all algorithm.
WHITE_SQUARE = { "WR1" : [8,1], "WN1" : [8,2], "WB1": [8,3], "WQ1" : [8,4],
			"WK1": [8,5], "WB2" : [8,6], "WN2": [8,7], "WR2": [8,8], 
			"WP1": [7,1], "WP2": [7,2], "WP3": [7,3], "WP4": [7,4],
			"WP5": [7,5], "WP6": [7,6], "WP7": [7,7], "WP8": [7,8]}

WHITE_COOR = { "WR1" : [0,0], "WN1" : [0,0], "WB1": [0,0], "WQ1" : [0,0],
			"WK1": [0,0], "WB2" : [0,0], "WN2": [0,0], "WR2": [0,0], 
			"WP1": [0,0], "WP2": [0,0], "WP3": [0,0], "WP4": [0,0],
			"WP5": [0,0], "WP6": [0,0], "WP7": [0,0], "WP8": [0,0]}

SQUARE_SIDE = 50.8

NUMBER_OF_PIECES = {"WR": 2, "WN": 2, "WB":2, "WK": 1, "WQ": 1, "WP": 8,
					"BR": 2, "BN": 2, "BB":2, "BK": 1, "BQ": 1, "BP": 8,}


# Calculate the expected destinate coordinate (mm) of black pe
def cal_destination_coordinates():

	# Calculate for black piece
	for key in BLACK_COOR:

		# Calculate y coordinate
		BLACK_COOR[key][0] = (BLACK_SQUARE[key][0]+ 1/2)*SQUARE_SIDE
		# Calculate x coordinate
		BLACK_COOR[key][1] = (BLACK_SQUARE[key][1]+ 1/2)*SQUARE_SIDE

	for key in WHITE_COOR:

		# Calculate y coordinate
		WHITE_COOR[key][0] = (WHITE_SQUARE[key][0]+ 1/2)*SQUARE_SIDE
		# Calculate x coordinate
		WHITE_COOR[key][1] = (WHITE_SQUARE[key][1]+ 1/2)*SQUARE_SIDE

def generate_input_board():

	rows, cols = (10, 10)

	square_board = [ ["NA" for i in range(cols)] for j in range(rows)]

	square_board[8][2] = "BN"
	square_board[1][5] = "WR"
	square_board[5][3] = "BK"
	square_board[2][5] = "BN"
	square_board[7][5] = "BP"
	square_board[2][7] = "BP"
	square_board[1][4] = "WP"
	square_board[0][4] = "WP"
	square_board[2][4] = "WP"
	square_board[0][5] = "BP"
	square_board[1][6] = "WP"
	square_board[0][6] = "WP"
	square_board[2][6] = "WP"
	square_board[4][8] = "WP"
	square_board[3][3] = "WP"


	print("Current board")
	print("    0      1     2    3     4     5     6     7     8     9 ")
	i = 0
	for row in square_board:
		print(str(i), end=" ")
		print(row)
		i = i+1

	return square_board

def generate_state_board():
	rows, cols = (10, 10)

	state_board = [ ["NR" for i in range(cols)] for j in range(rows)]

	return state_board

def print_board(this_board):
	print("    0      1     2    3     4     5     6     7     8     9 ")
	i = 0
	for row in this_board:
		print(str(i), end=" ")
		print(row)
		i = i+1


# This function generates an array storing the positions of pieces.
# The array will be received from image processing
def generate_piece_position():
	piece_position = []
	# piece_position.append(piece.Piece("WK", 3, 7, 177.8, 381))
	# piece_position.append(piece.Piece("WK", 1, 1, 76.2, 76.2))
	piece_position.append(piece.Piece("BN", 8, 2))
	piece_position.append(piece.Piece("WR", 1, 5))
	piece_position.append(piece.Piece("BK", 5, 3))
	piece_position.append(piece.Piece("BN", 2, 5))
	piece_position.append(piece.Piece("BP", 7, 5))
	piece_position.append(piece.Piece("BP", 2, 7))
	piece_position.append(piece.Piece("WP", 1, 4))
	piece_position.append(piece.Piece("WP", 0, 4))
	piece_position.append(piece.Piece("WP", 2, 4))
	piece_position.append(piece.Piece("BP", 0, 5))
	piece_position.append(piece.Piece("WP", 1, 6))
	piece_position.append(piece.Piece("WP", 0, 6))
	piece_position.append(piece.Piece("WP", 2, 6))
	piece_position.append(piece.Piece("WP", 4, 8))
	piece_position.append(piece.Piece("WP", 3, 3))

	return piece_position

# This function generates a full piece name from the symbol name.
# It supports to throw errors and exception.
def generate_string_piece_name(piece_name):
	this_name = ""
	
	if piece_name[0] == "B":
		this_name = this_name + "black "
	else:
		this_name = this_name + "white "
	
	if piece_name[1] == "K":
		this_name = this_name + "king"
	elif piece_name[1] == "Q":
		this_name = this_name + "queen"
	elif piece_name[1] == "N":
		this_name = this_name + "knight"
	elif piece_name[1] == "B":
		this_name = this_name + "bishop"
	elif piece_name[1] == "R":
		this_name = this_name + "rook"
	else:
		this_name = this_name + "pawn"

	return this_name 


# This function changes and updates a piece name in piece_dictionary and 
# current_board. It also throws exception if there are more pieces than
# normal for a specific piece. For example, if there are more than 2 black 
# knight on the current board, the function would throw an exception.

def update_name_in_piece_dictionary_current_board(this_piece, max_index, piece_dict, current_board, current_piece_amount):

	i = current_piece_amount[this_piece.name]

	while(i<=max_index):
		key = this_piece.name + str(i)
		i = i+1

		# If this index does not exist in the dictionary,
		# add index to the piece name, update the new name in
		# current board and add the piece to the dictionary
		if piece_dict.get(key) == None:
			this_piece.name = key
			piece_dict[key] = this_piece
			
			current_board[this_piece.row][this_piece.col] = key
			
			return

	full_piece_name = generate_string_piece_name(this_piece.name)
	raise Exception("There are more than " + str(max_index) + " " + full_piece_name)


# This function returns check if a targeted piece is at its destination
# If it is not, return the closest destination to it.
def check_pieces_in_the_right_position (piece, piece_dictionary, current_board, current_piece_amount):
	# declare a temporary dictionary
	dest_square = {}
	delta_x = [0 for i in range (8)]
	delta_y = [0 for i in range (8)]

	min_distance = 99999
	dest_row = 0
	dest_col = 0
	occupied = False

	# check if this piece is black or white
	if (piece.name[0] == "B"):
		# assign BLACK_SQUARE to dest_square if this is a black piece
		dest_square = BLACK_SQUARE
		
	else:
		# else assign WHITE_SQUARE to dest_square
		dest_square = WHITE_SQUARE


	max_index = NUMBER_OF_PIECES[piece.name]
	
	update_name_in_piece_dictionary_current_board(piece, max_index, piece_dictionary, current_board, current_piece_amount)
	
	i = 1
	while (i <= max_index):

		key = piece.name[0:2] + str(i)

		# Look up in the dest_square to find the position of key
		row = dest_square[key][0]
		col = dest_square[key][1]
		current_piece = current_board[row][col] # This is a string. Nme of a piece at this position

		i = i+1

		# The piece is at its right destination
		if row == piece.row and col == piece.col:
			return True, row, col, None, None

		else:

			# Check if the current piece at row and col is the twin
			# of the target piece.
			if current_piece[0:2] == piece.name[0:2]:
				# If it is true, do nothing.
				continue

			# If the current_piece is not the twin of the target piece,
			# calculate the distance from the target piece to this detination.
			sum_distance = abs(piece.row - row) + abs(piece.col - col)

			if sum_distance < min_distance:
				dest_row = row
				dest_col = col
				min_distance = sum_distance
				occupied = False

				# Check if there is a piece occupying in this destination
				if current_piece != "NA":
					occupied = True
			

	return False, dest_row, dest_col, occupied, min_distance

# This function uses to find the optimal piece to rearrange in the 32 pieces.
# Rules to be an optimal piece:
#  -Have the minimum distance (delta_x + delta_y)
#  -Prioritize the inner pieces
def pick_a_piece(piece_list, state_board, current_board, piece_dictionary):

	board_rearranged = True
	min_distance = 99999
	piece_to_arrange = piece.Piece()

	# The dictionary tracks the number of pieces in the current board.
	current_piece_amount = {"WR": 0, "WN": 0, "WB":0, "WK": 0, "WQ": 0, "WP": 0,
					"BR": 0, "BN": 0, "BB": 0, "BK": 0, "BQ": 0, "BP": 0}

	for this_piece in piece_list:
		# print("-----------------------")
		# print(this_piece)
		
		if current_piece_amount.get(this_piece.name) != None:
			current_piece_amount[this_piece.name] += 1
		else:
			raise Exception("A piece name is not legit.")

		piece_rearranged, dest_row, dest_col, dest_occupied, expected_dist = check_pieces_in_the_right_position(this_piece, piece_dictionary, current_board, current_piece_amount)
		
		# if this piece is at the right position, set "RA" at its position
		# in the state_board
		if piece_rearranged:
			state_board[dest_row][dest_col] = "RA"
			# print("The piece is at the right position.")
			continue

		board_rearranged = False

		# if expected_dist > min_distance:
		# 	# print("expected_dist is bigger than min_distance")
		# 	continue

		# if piece_to_arrange.name != None:
		# 	if this_piece.name[1] == "P" and piece_to_arrange.name[1] != "P":
		# 		# print("the current optimal piece is not a pawn:")
		# 		# print(piece_to_arrange)
		# 		continue

		if piece_to_arrange.name != None:
			if  ( piece_to_arrange.name[1] == "P" and this_piece.name[1] != "P" ) == False:

				if expected_dist > min_distance:
					continue

				if this_piece.name[1] == "P" and piece_to_arrange.name[1] != "P":
					continue



		min_distance = expected_dist
		piece_to_arrange.name = this_piece.name
		piece_to_arrange.row = this_piece.row
		piece_to_arrange.col = this_piece.col
		piece_to_arrange.x_coor = this_piece.x_coor
		piece_to_arrange.y_coor = this_piece.y_coor
		piece_to_arrange.dest_row = dest_row
		piece_to_arrange.dest_col = dest_col
		piece_to_arrange.dest_occupied = dest_occupied
		# print("replaced the optimal piece.")
		# print(piece_to_arrange)

	error_message = ""

	# # This block of code to check if there are 32 pieces. We may need to consider the second block instead if 
	# # it does not take too much time.
	# if len(dict) != 32:
	# 	error_message = "Missing pieces"

	# This block of code to support debug
	# print("the number of pieces")
	# for key in current_piece_amount:
	# 	print(key + ": " + str(current_piece_amount[key]))

	# 	if current_piece_amount[key] != NUMBER_OF_PIECES[key]:
	# 		piece_full_name = generate_string_piece_name(key)
	# 		error_message = error_message + "\n" + "Missing " + str(NUMBER_OF_PIECES[key] - current_piece_amount[key]) + " " + piece_full_name + " pieces."
	###################################
	
	if error_message != "":
		raise Exception(error_message)
	
	return board_rearranged, piece_to_arrange


# This function finds the closest edge to move a piece from current square
# to the middle of squares.
def find_the_closest_edge(current_square, dest_square, row):
	delta = dest_square - current_square

	if delta < 0:

		if row:
			return "left", current_square
		else:
			return "down", current_square

	else:

		if row:
			return "right", current_square+1
		else:
			return "up", current_square+1


# This function calculates the edge coordinate. It can be a row edge 
# or a col edge. The formula is still the same.
def cal_edge_coor(this_edge):

	return this_edge*SQUARE_SIDE

# This function calculates the number of steps to move from 
# current_coor to new_coor.
def cal_steps(current_coor, new_coor, corexy):
	return math.ceil(corexy.step_per_mm * abs(new_coor - current_coor))

def find_closest_edge_to_dest(current_square, dest_square, row):
	delta = dest_square - current_square

	if delta < 0:

		if row:
			return "left", dest_square+1
	else:

		if row:
			return "right", dest_square

# This function calculates the destination coordinates from
# the destination square.
def cal_destination_coor(dest_row, dest_col):
	x_coor = ( dest_row + 1/2) * SQUARE_SIDE
	y_coor = ( dest_col + 1/2) *SQUARE_SIDE
	return x_coor, y_coor

# This function calculates the directions and the number of steps
# to move from the current point to the destination point.
def find_dir_step_to_dest_point(current_x_coor, current_y_coor, new_x_coor, new_y_coor, corexy):

	# print("current x: " + str(current_x_coor))
	# print("current y: " + str(current_y_coor))
	delta_x = new_x_coor-current_x_coor 	# in mm
	delta_y = new_y_coor-current_y_coor		# in mm

	steps_in_x = math.ceil(corexy.step_per_mm * abs(delta_x)) + 30
	steps_in_y = math.ceil(corexy.step_per_mm * abs(delta_y)) + 10 

	dir_in_x = "right"
	dir_in_y = "up"

	if delta_x < 0:
		dir_in_x = "left"
	
	if delta_y < 0:
		dir_in_y = "down"
	
	return dir_in_x, steps_in_x, dir_in_y, steps_in_y

def capture_a_piece(this_piece, corexy, movementQueue):
	# new_x_coor, new_y_coor = cal_destination_coor(this_piece.row, this_piece.col)
	print("Capture: " + str(this_piece))
	new_x_coor = float(this_piece.x_coor)
	new_y_coor = float(this_piece.y_coor)
	delta_x = new_x_coor-corexy.current_x 		# in mm
	delta_y = new_y_coor-corexy.current_y		# in mm

	steps_in_x = math.floor(corexy.step_per_mm * abs(delta_x))
	steps_in_y = math.floor(corexy.step_per_mm * abs(delta_y))

	if delta_x < 0:
		movementQueue.append(movement.Movement(True, False, "left", steps_in_x, new_x_coor, corexy.current_y))
		
	else:
		movementQueue.append(movement.Movement(True, False, "right", steps_in_x, new_x_coor, corexy.current_y))
		
	
	corexy.current_x = new_x_coor
	
	if delta_y < 0:
		movementQueue.append(movement.Movement(True, False,"down", steps_in_y, corexy.current_x, new_y_coor))

	else:
		movementQueue.append(movement.Movement(True, False,"up", steps_in_y, corexy.current_x, new_y_coor))

	corexy.current_y = new_y_coor
	

# The function creates a move to 
# the closest horizontal (parallel to x axis) edge
def move_to_the_closest_horizontal_edge(piece, current_col, new_col, corexy, movementQueue):
	delta = new_col - current_col
	this_direction = "up"
	this_edge = current_col+1

	if delta < 0:
		this_direction = "down"
		this_edge = current_col

	print("move " + piece.name + " " + this_direction + " to horizontal edge " + str(this_edge))
	this_edge_coor = cal_edge_coor(this_edge)
	step_count = cal_steps(corexy.current_y, this_edge_coor, corexy)
	movementQueue.append(movement.Movement(True, False, this_direction, step_count, corexy.current_x, this_edge_coor))
	#update y_coor for corexy and piece
	corexy.current_y = this_edge_coor
	piece.y_coor = this_edge_coor

# The function creates a move to the
# closest vertical edge to the destination square.
# vertical edge parallel to y_axis
def move_to_the_closest_vertical_edge_to_dest(piece, current_row, dest_row, corexy, movementQueue):
	print("move to the closest vertical edge to dest")
	print(str(piece))
	print("current row: " + str(current_row))
	print("dest row: " + str(dest_row))
	
	# determine which edge to move to
	delta = dest_row - current_row
	# this_direction = "right"
	this_edge = dest_row

	if delta < 0:
		# this_direction = "left"
		this_edge = dest_row +1

	#determine which direction to move
	print("vertical edge: " + str(this_edge))
	this_edge_coor = cal_edge_coor(this_edge)
	print("vertical edge coor: " + str(this_edge_coor))
	delta_edge_coor = this_edge_coor - piece.x_coor
	this_direction = "right"
	if delta_edge_coor < 0:
		this_direction ="left"

	print("current x: " + str(corexy.current_x))
	print("current piece x: " + str(piece.x_coor))
	step_count = cal_steps(corexy.current_x, this_edge_coor, corexy)
	print("step counts: " + str(step_count))
	movementQueue.append(movement.Movement(True, False, this_direction, step_count, this_edge_coor, corexy.current_y))
	# update x_coor for corexy and piece
	corexy.current_x = this_edge_coor
	piece.x_coor = this_edge_coor

# The function creates a move to the destination point of a piece
def move_to_the_destination_point(piece, corexy, movementQueue):
	dest_x_coor, dest_y_coor = cal_destination_coor(piece.dest_row, piece.dest_col)
	dir_in_x, steps_in_x, dir_in_y, steps_in_y = find_dir_step_to_dest_point(piece.x_coor, piece.y_coor, dest_x_coor, dest_y_coor, corexy)
	print(str(piece.x_coor))
	print(str(piece.y_coor))
	print(str(dest_x_coor))
	print(str(dest_y_coor))
	# print(str(dir_in_x) + ", " + str(steps_in_x))
	# print(str(dir_in_y) + ", " + str(steps_in_y))
	movementQueue.append(movement.Movement(True, False, dir_in_y, steps_in_y, corexy.current_x, dest_y_coor))
	corexy.current_y = dest_y_coor
	movementQueue.append(movement.Movement(True, False, dir_in_x, steps_in_x, dest_x_coor, corexy.current_y))
	corexy.current_x = dest_x_coor


def find_empty_square(current_row, current_col, current_board):

	left_exist = True
	right_exist = True
	up_exist = True
	down_exist = True

	# check if there are squares on the left of current square
	if (current_col-1) < 0:
		left_exist = False

	# check if there are squares on the right of current square
	if (current_col+1) > 10:
		right_exist = False

	# check if there are squares above current square
	if (current_row -1) < 0:
		up_exist = False

	# check if there are squares below current square
	if (current_row +1) > 10:
		down_exist = False

	if left_exist:

		# check if the square on left of current square is empty
		if current_board[current_row][current_col -1] == "NA" :
			return current_row, current_col-1

		# check if the square on the left upper corner of current square is empty
		if up_exist:
			if current_board[current_row-1][current_col-1] == "NA":
				return current_row-1, current_col-1

		# check if the square on the left down corner of current square is empty
		if down_exist:
			if current_board[current_row+1][current_col-1] == "NA":
				return current_row+1, current_col-1

	# check if the square above current square is empty
	if up_exist:
		if current_board[current_row-1][current_col] == "NA":
			return current_row-1, current_col

	# check if the square below current square is empty
	if down_exist:
		if current_board[current_row+1][current_col] == "NA":
			return current_row+1, current_col

	if right_exist:

		# check if the square on the right current square is empty
		if current_board[current_row][current_col+1] == "NA":
			return current_row, current_col+1

		# check if the square on the right upper corner of current square is empty
		if up_exist:
			if current_board[current_row-1][current_col+1] == "NA":
				return current_row-1, current_col+1

		# check if the square on the right below corner of current square is empty
		if down_exist:
			if current_board[current_row+1][current_col+1] == "NA":
				return current_row+1, current_col+1

	if left_exist:
		return find_empty_square(current_row, current_col-1, current_board)
	if up_exist:
		return find_empty_square(current_row-1, current_col, current_board)
	if down_exist:
		return find_empty_square(current_row+1, current_col, current_board)
	if right_exist:
		return find_empty_square(current_row, current_col+1, current_board)
	if left_exist and up_exist:
		return find_empty_square(current_row-1, current_col-1, current_board)
	if left_exist and down_exist:
		return find_empty_square(current_row+1, current_col-1, current_board)
	if right_exist and up_exist:
		return find_empty_square(current_row-1, current_col+1, current_board)
	if right_exist and down_exist:
		return find_empty_square(current_row+1, current_col+1, current_board)

# The function finds an empty square to move a piece there and
# put the result col and row in the dest_col and dest_row of the piece.
# The general alogrithm is breadth-first-search.
def find_empty_spot(piece, current_board):

	piece.dest_row, piece.dest_col = find_empty_square(piece.row, piece.col, current_board)
	return piece.dest_row, piece.dest_col

# This function creates moves to move a piece from its current
# position to another position
def move_a_piece(piece, corexy, movementQueue):
	capture_a_piece(piece, corexy, movementQueue)

	# turn on the electro magnet to capture the piece
	movementQueue.append(movement.Movement(False, True))
	
	move_to_the_closest_horizontal_edge(piece, piece.col, piece.dest_col, corexy, movementQueue)
	move_to_the_closest_vertical_edge_to_dest(piece, piece.row, piece.dest_row, corexy, movementQueue)
	move_to_the_destination_point(piece, corexy, movementQueue)

	# turn off the electro magnet to release the piece
	movementQueue.append(movement.Movement(False, False))



# The function rearranges a piece and adds moves to the movementQueue.
def rearrange_piece(piece, corexy, movementQueue, piece_dictionary, current_board):
	# Save the current positions of piece and corexy to
	# to recover at the end of the function
	old_piece_row = piece.row
	old_piece_col = piece.col
	old_piece_x_coor = piece.x_coor
	old_piece_y_coor = piece.y_coor
	old_corexy_x_coor = corexy.current_x
	old_corexy_y_coor = corexy.current_y

	# Check if the destination is occupied.
	# If it is occupied, find an empty square and move the 
	# occupied piece there.
	if piece.dest_occupied:
		occupied_piece_name = current_board[piece.dest_row][piece.dest_col]
		occupied_piece = piece_dictionary[occupied_piece_name]
		print("Occupied piece: " + str(occupied_piece))
		find_empty_spot(occupied_piece, current_board)
		move_a_piece(occupied_piece, corexy, movementQueue)

	move_a_piece(piece, corexy, movementQueue)

	# Recover the orginal values of the piece and corexy
	piece.x_coor = old_piece_x_coor
	piece.y_coor = old_piece_y_coor
	piece.row = old_piece_row
	piece.col = old_piece_col
	corexy.current_x = old_corexy_x_coor
	corexy.current_y = old_corexy_y_coor
	
def generate_input():
    
    myCamera = cameraDriver.ReChessCamera()
    myCamera.takeAPicture()
    current_board, piece_list = getAbstraction()
    
	# Check unless there are 32 pieces, the camera keeps taking pictures.
	# TODO: if the error LED works, we should consider take this block of code out.
    # while(len(piece_list) != 32):
    #     myCamera.takeAPicture()
    #     current_board, piece_list = getAbstraction()

    myCamera.closeCamera()

    state_board = generate_state_board()
    current_board = [list(row) for row in current_board]
    return current_board, piece_list, state_board


def start_rearrange(corexy, this_fsm):

	# # Create a core xy
	# corexy = corexyLib.CoreXY(20, 'Half', motorLib.Motor(20, 21, 1, (14, 15, 18), 400, 'Half'), 
	# 	motorLib.Motor(19, 26, 1, (14, 15, 18), 400, 'Half'), 
	# 	eMagnetLib.EMagnet(5),0, 0)
	# # Set up the corexy
	# corexy.set_up()

	movementQueue = []
	piece_dictionary = {}
	manualy_stop = False

	try:
		current_board, piece_list, state_board = generate_input()
		print_board(current_board)
		board_rearranged, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

		while board_rearranged == False and manualy_stop == False:

			# Check if the button is pressed to stop the rearrange.
			if not this_fsm.running:
					print("Button is pressed to stop the rearrange")
					# TODO:change from move_to(0,0) to move_to_origin later
					# corexy.move_to_origin()
					corexy.move_to(0,0)
					return

			print("Board is not rearranged.")
			print("Piece to arrange:")
			print(piece_to_arrange)

			# If there are 3 pieces moved, reset the origin to advoid losing steps.
			if this_fsm.piece_count >= 4:
				print("Reset to origin because there are 4 pieces move.")
				# TODO:change from move_to(0,0) to move_to_origin later
				# corexy.move_to_origin()
				corexy.move_to(0,0)
				this_fsm.piece_count = 0
			
			# Create movement queue to rearrange piece
			rearrange_piece(piece_to_arrange, corexy, movementQueue, piece_dictionary, current_board)

			for this_move in movementQueue:
				print(this_move)
				corexy.make_a_move(this_move)
				if not this_fsm.running:
					print("Button is pressed to stop the rearrange")
					manualy_stop = True
					# TODO:change from move_to(0,0) to move_to_origin later
					# corexy.move_to_origin()
					corexy.move_to(0,0)
					
					return
			
			# Increment piece_count of the fsm
			this_fsm.piece_count += 1

			# Take current board input from the image processing
			current_board, piece_list, state_board = generate_input()
			print_board(current_board)
			movementQueue = []
			piece_dictionary = {}

			# clean up memory
			gc.collect()

			board_rearranged, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

		if (board_rearranged):
			print("Board is rearranged")
			# TODO:change from move_to(0,0) to move_to_origin later
			# corexy.move_to_origin()
			corexy.move_to(0,0)

			# Update FSM to end the system
			this_fsm.running = False
			this_fsm.not_start = True
			this_fsm.piece_count = 0
			print("end the system")
			

	except Exception as e:
		print(e)

# def start_rearrange(corexy, this_fsm):

# 	while True:
        
# 		if this_fsm.running:
# 			rearrange(corexy)
	

# cal_destination_coordinates()
# # print(BLACK_DEST)

# current_board = generate_input_board()

# piece_list = generate_piece_position()
# state_board = generate_state_board()

# print("Stateboard before:")
# print_board(state_board)

# piece_dictionary = {}

# try:

# 	board_rearranged, min_distance, piece_to_arrange = pick_a_piece(piece_list, state_board, current_board, piece_dictionary)

# 	print("piece dictionary:")
# 	for key in piece_dictionary:
# 		print(key + ": " + str(piece_dictionary[key].name))

# 	print("Current board: ")
# 	print_board(current_board)
# 	print("Piece to arrange:")
# 	print(piece_to_arrange)
# 	if piece_to_arrange.dest_occupied:
# 		print("The destination is occupied.")
# 	else:
# 		print("The destination is not occupied.")

# except Exception as e:
# 	print(e)

	# TODO: ADD BLINKING ERROR LIGHT


