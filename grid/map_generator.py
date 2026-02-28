
import random

def generate_random_map(grid, density):
	for row in range(grid.rows):
		for col in range(grid.cols):
			if grid.grid[row][col] == 0:
				if random.random() < density:
					grid.add_obstacle(row, col)
