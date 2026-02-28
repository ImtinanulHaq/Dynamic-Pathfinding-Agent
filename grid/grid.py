
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.goal = None

    def set_start(self, row, col):
        if self.start is not None:
            old_r, old_c = self.start
            if self.grid[old_r][old_c] == 2:
                self.grid[old_r][old_c] = 0
        self.start = (row, col)
        self.grid[row][col] = 2

    def set_goal(self, row, col):
        if self.goal is not None:
            old_r, old_c = self.goal
            if self.grid[old_r][old_c] == 3:
                self.grid[old_r][old_c] = 0
        self.goal = (row, col)
        self.grid[row][col] = 3

    def add_obstacle(self, row, col):
        if self.grid[row][col] == 0:
            self.grid[row][col] = 1

    def remove_obstacle(self, row, col):
        if self.grid[row][col] == 1:
            self.grid[row][col] = 0

    def is_obstacle(self, row, col):
        return self.grid[row][col] == 1

    def reset(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.goal = None
