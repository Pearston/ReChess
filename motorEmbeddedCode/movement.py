

class Movement:

	def __init__ (self, this_is_step = True, this_eMagnet_on = False, this_direction=None, this_step_count=None, dest_x=None, dest_y=None):
		self.is_step = this_is_step
		self.eMagnet_on = this_eMagnet_on
		self.direction = this_direction
		self.step_count = this_step_count
		self.dest_x = dest_x
		self.dest_y = dest_y
		

	def __str__ (self):
		return f"{self.is_step} , {self.eMagnet_on}, {self.direction}, {self.step_count}, {self.dest_x}, {self.dest_y} "




