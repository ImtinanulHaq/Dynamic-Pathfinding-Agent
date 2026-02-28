
import tkinter as tk
import random

from algorithms.astar.astar import astar
from algorithms.gbfs.gbfs import gbfs
from metrics.metrics import Metrics


class GridGUI:
    def __init__(self, grid, cell_size=30):
        self.grid = grid
        self.cell_size = cell_size
        self.path = None
        self.running = False

        self.root = tk.Tk()
        self.root.title("Dynamic Pathfinding Agent")

        self.canvas = tk.Canvas(
            self.root,
            width=grid.cols * cell_size,
            height=grid.rows * cell_size,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        self.algo_var = tk.StringVar(value="A*")
        tk.Label(controls, text="Algorithm:").pack(side=tk.LEFT)
        tk.OptionMenu(controls, self.algo_var, "A*", "GBFS").pack(side=tk.LEFT)

        self.heuristic_var = tk.StringVar(value="manhattan")
        tk.Label(controls, text="Heuristic:").pack(side=tk.LEFT)
        tk.OptionMenu(controls, self.heuristic_var, "manhattan", "euclidean").pack(side=tk.LEFT)

        self.dynamic_var = tk.BooleanVar(value=False)
        tk.Checkbutton(controls, text="Dynamic Obstacles", variable=self.dynamic_var).pack(side=tk.LEFT)

        tk.Button(controls, text="Run", command=self.run_search).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Reset", command=self.reset_all).pack(side=tk.LEFT, padx=5)

        self.metrics = Metrics()
        self.metrics_label = tk.Label(self.root, text="Nodes: 0 | Path: 0 | Time: 0 ms")
        self.metrics_label.pack()

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"
                if self.grid.grid[r][c] == 1:
                    color = "black"
                elif self.grid.grid[r][c] == 2:
                    color = "orange"
                elif self.grid.grid[r][c] == 3:
                    color = "green"

                if self.path and (r, c) in self.path:
                    if (r, c) != self.grid.start and (r, c) != self.grid.goal:
                        color = "yellow"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

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

        self.metrics.reset()
        self.metrics.start_timer()

        algo = self.algo_var.get()
        heuristic = self.heuristic_var.get()

        if algo == "A*":
            path = astar(self.grid, heuristic)
        else:
            path = gbfs(self.grid, heuristic)

        self.metrics.stop_timer()

        if path:
            self.metrics.path_cost = len(path) - 1
            self.metrics.nodes_visited = len(path)
            if self.dynamic_var.get():
                self.path = []
                self.running = True
                self.animate_step(path, 0)
            else:
                self.path = path
                self.draw_grid()
        else:
            self.path = None
            self.metrics.path_cost = 0
            self.metrics.nodes_visited = 0
            self.draw_grid()

        self.update_metrics_label()

    def animate_step(self, path, idx):
        if idx >= len(path):
            self.running = False
            return

        current = path[idx]

        if self.grid.is_obstacle(current[0], current[1]) and idx > 0:
            self.grid.set_start(path[idx - 1][0], path[idx - 1][1])
            algo = self.algo_var.get()
            heuristic = self.heuristic_var.get()
            if algo == "A*":
                new_path = astar(self.grid, heuristic)
            else:
                new_path = gbfs(self.grid, heuristic)
            if new_path:
                self.animate_step(new_path, 0)
            else:
                self.running = False
            return

        self.path = path[: idx + 1]
        self.draw_grid()

        if random.random() < 0.15 and self.dynamic_var.get():
            self.spawn_random_obstacle(path, idx)
            self.draw_grid()

        self.root.after(150, self.animate_step, path, idx + 1)

    def spawn_random_obstacle(self, path, idx):
        future_path = set(path[idx:])
        for _ in range(10):
            r = random.randint(0, self.grid.rows - 1)
            c = random.randint(0, self.grid.cols - 1)
            if self.grid.grid[r][c] == 0 and (r, c) not in future_path:
                self.grid.add_obstacle(r, c)
                break

    def update_metrics_label(self):
        text = f"Nodes: {self.metrics.nodes_visited} | Path: {self.metrics.path_cost} | Time: {int(self.metrics.get_execution_time())} ms"
        self.metrics_label.config(text=text)

    def reset_all(self):
        self.running = False
        self.path = None
        self.grid.reset()
        self.grid.set_start(0, 0)
        self.grid.set_goal(self.grid.rows - 1, self.grid.cols - 1)
        self.metrics.reset()
        self.update_metrics_label()
        self.draw_grid()

    def run(self):
        self.root.mainloop()
