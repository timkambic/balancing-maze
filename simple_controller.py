# simple controller for both axis combined
class Controller_simple():
	def __init__(self):
		self.previous_direction =0 # not used
		self.speed = 10 # not used
		self.max_angle = 20 
		self.min_angle = 10
		self.limit_to_move_x = 25 # used in if statement to decide whether to move specific axis or not
		self.limit_to_move_y = 25
		
	def SetParameters(self,speed, max_angle,min_angle):
		self.speed = speed
		self.max_angle = max_angle
		self.min_angle = min_angle
		
	def Compute(self, error_x,error_y):
		self.output_x = 13
		if error_x > self.limit_to_move_x:
			self.output_x = 22
		if error_x < -self.limit_to_move_x:
			self.output_x = 5
			
		self.output_y = 17
		if error_y > self.limit_to_move_y:
			self.output_y = 7 # inverted y-axis
		if error_y < -self.limit_to_move_y:
			self.output_y = 24
		
		return self.output_x, self.output_y
		

