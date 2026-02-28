
import tkinter as tk

from algorithms.astar.astar import astar
from algorithms.gbfs.gbfs import gbfs
from metrics.metrics import Metrics

import random
import threading

class GridGUI:
	def __init__(self, grid, cell_size=30):
		self.grid = grid
		self.cell_size = cell_size
		self.root = tk.Tk()
		self.root.title('Dynamic Pathfinding Agent')
		self.canvas = tk.Canvas(self.root, width=grid.cols*cell_size, height=grid.rows*cell_size)
		self.canvas.pack()
		self.canvas.bind('<Button-1>', self.on_click)

		self.algo_var = tk.StringVar(value='A*')
		self.heuristic_var = tk.StringVar(value='manhattan')
		self.metrics = Metrics()

		algo_frame = tk.Frame(self.root)
		algo_frame.pack()
		tk.Label(algo_frame, text='Algorithm:').pack(side=tk.LEFT)
		tk.OptionMenu(algo_frame, self.algo_var, 'A*', 'GBFS').pack(side=tk.LEFT)
		tk.Label(algo_frame, text='Heuristic:').pack(side=tk.LEFT)
		tk.OptionMenu(algo_frame, self.heuristic_var, 'manhattan', 'euclidean').pack(side=tk.LEFT)
		tk.Button(algo_frame, text='Run', command=self.run_search).pack(side=tk.LEFT)

		self.metrics_label = tk.Label(self.root, text='Nodes: 0 | Path: 0 | Time: 0 ms')
		self.metrics_label.pack()

	self.dynamic_mode = tk.BooleanVar(value=False)
	tk.Checkbutton(self.root, text='Dynamic Obstacles', variable=self.dynamic_mode).pack()
	self.running = False
	self.draw_grid()

	def draw_grid(self, path=None):
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
				if path and (r, c) in path:
					color = 'yellow' if (r, c) != self.grid.start and (r, c) != self.grid.goal else color
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

	def run_search(self):
		if self.running:
			return
		self.running = True
		self.metrics.reset()
		self.metrics.start_timer()
		algo = self.algo_var.get()
		heuristic = self.heuristic_var.get()
		if algo == 'A*':
			path = astar(self.grid, heuristic)
		else:
			path = gbfs(self.grid, heuristic)
		self.metrics.stop_timer()
		if path:
			self.metrics.path_cost = len(path)
			self.metrics.nodes_visited = len(set(path))
			if self.dynamic_mode.get():
				threading.Thread(target=self.animate_path_with_dynamic_obstacles, args=(path,)).start()
			else:
				self.draw_grid(path)
		else:
			self.metrics.path_cost = 0
			self.metrics.nodes_visited = 0
			self.draw_grid()
		self.metrics_label.config(text=f'Nodes: {self.metrics.nodes_visited} | Path: {self.metrics.path_cost} | Time: {int(self.metrics.get_execution_time())} ms')
		self.running = False

	def animate_path_with_dynamic_obstacles(self, path):
		for idx, pos in enumerate(path):
			if idx == 0:
				continue
			if random.random() < 0.15:
				self.spawn_random_obstacle(path, idx)
			self.draw_grid(path[:idx+1])
			self.root.update()
			self.root.after(100)
			if self.grid.is_obstacle(*pos):
				new_path = self.replan_from(pos)
				if new_path:
					self.animate_path_with_dynamic_obstacles(new_path)
				return

	def spawn_random_obstacle(self, path, idx):
		for _ in range(10):
			r = random.randint(0, self.grid.rows-1)
			c = random.randint(0, self.grid.cols-1)
			if self.grid.grid[r][c] == 0 and (r, c) not in path[idx:]:
				self.grid.add_obstacle(r, c)
				break

	def replan_from(self, pos):
		algo = self.algo_var.get()
		heuristic = self.heuristic_var.get()
		self.grid.set_start(*pos)
		if algo == 'A*':
			return astar(self.grid, heuristic)
		else:
			return gbfs(self.grid, heuristic)

	def run(self):
		self.root.mainloop()
