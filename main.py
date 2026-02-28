
from grid.grid import Grid
from grid.map_generator import generate_random_map
from gui.gui import GridGUI

def main():
	rows, cols = 15, 20
	grid = Grid(rows, cols)
	grid.set_start(0, 0)
	grid.set_goal(rows-1, cols-1)
	generate_random_map(grid, density=0.2)
	gui = GridGUI(grid)
	gui.run()

if __name__ == '__main__':
	main()
