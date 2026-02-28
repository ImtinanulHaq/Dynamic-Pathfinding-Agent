
import tkinter as tk

class GridGUI:
	def __init__(self, grid, cell_size=30):
		self.grid = grid
		self.cell_size = cell_size
		self.root = tk.Tk()
		self.root.title('Dynamic Pathfinding Agent')
		self.canvas = tk.Canvas(self.root, width=grid.cols*cell_size, height=grid.rows*cell_size)
		self.canvas.pack()
		self.canvas.bind('<Button-1>', self.on_click)
		self.draw_grid()

	def draw_grid(self):
		self.canvas.delete('all')
		for r in range(self.grid.rows):
			for c in range(self.grid.cols):
				x1 = c * self.cell_size
				y1 = r * self.cell_size
				x2 = x1 + self.cell_size
				y2 = y1 + self.cell_size
				color = 'white'
				if self.grid.grid[r][c] == 1:
					color = 'black'
				elif self.grid.grid[r][c] == 2:
					color = 'orange'
				elif self.grid.grid[r][c] == 3:
					color = 'green'
				self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

	def on_click(self, event):
		row = event.y // self.cell_size
		col = event.x // self.cell_size
		if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
			if self.grid.grid[row][col] == 0:
				self.grid.add_obstacle(row, col)
			elif self.grid.grid[row][col] == 1:
				self.grid.remove_obstacle(row, col)
			self.draw_grid()

	def run(self):
		self.root.mainloop()
