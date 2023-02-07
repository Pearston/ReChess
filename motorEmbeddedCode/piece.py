# This is the class for chess piece

class Piece:

	# row, col, x_coor, y_coor is the current position of the piece
	# based on square and mm coordinate
	def __init__(self, name=None, row =None, col=None, x_coor=None, y_coor=None, dest_row=None, dest_col=None, dest_occupied=None):
		self.name = name
		self.row = row
		self.col = col
		self.x_coor = x_coor
		self.y_coor = y_coor
		self.dest_row = dest_row
		self.dest_col = dest_col
		self.dest_occupied = dest_occupied

	def __str__(self):
		return f"{self.name}, current_square({self.row}, {self.col}), current_coor({self.x_coor}, {self.y_coor}), dest_square({self.dest_row}, {self.dest_col}), {self.dest_occupied} "
	
	def update_row(self, new_row):
		self.row = new_row

	def update_col(self, new_col):
		self.col = new_col

	def update_x_coor(self, new_x_coor):
		self.x_coor = new_x_coor

	def update_y_coor(self, new_y_coor):
		self.y_coor = new_y_coor



