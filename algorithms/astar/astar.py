
import heapq
from algorithms.heuristics import manhattan, euclidean

def astar(grid, heuristic='manhattan'):
	start = grid.start
	goal = grid.goal
	if heuristic == 'manhattan':
		h = manhattan
	else:
		h = euclidean

	open_set = []
	heapq.heappush(open_set, (0 + h(start, goal), 0, start, [start]))
	visited = set()

	while open_set:
		f, g, current, path = heapq.heappop(open_set)
		if current == goal:
			return path
		if current in visited:
			continue
		visited.add(current)
		for d in [(-1,0),(1,0),(0,-1),(0,1)]:
			nr, nc = current[0]+d[0], current[1]+d[1]
			if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
				if not grid.is_obstacle(nr, nc) and (nr, nc) not in visited:
					heapq.heappush(open_set, (g+1+h((nr,nc), goal), g+1, (nr,nc), path+[(nr,nc)]))
	return None
