
class MapEditor:
	def __init__(self, grid):
		self.grid = grid

	def toggle_obstacle(self, row, col):
		if self.grid.is_obstacle(row, col):
			self.grid.remove_obstacle(row, col)
		else:
			self.grid.add_obstacle(row, col)
