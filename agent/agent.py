
class Agent:
	def __init__(self, grid):
		self.grid = grid
		self.position = grid.start

	def move_to(self, row, col):
		if not self.grid.is_obstacle(row, col):
			self.position = (row, col)
