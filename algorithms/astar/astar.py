
import heapq
from algorithms.heuristics import manhattan, euclidean

def astar(grid, heuristic='manhattan'):
    start = grid.start
    goal = grid.goal

    if start is None or goal is None:
        return None

    if heuristic == 'manhattan':
        h = manhattan
    else:
        h = euclidean

    counter = 0
    open_set = []
    heapq.heappush(open_set, (h(start, goal), counter, 0, start, [start]))
    visited = set()

    while open_set:
        f, _, g, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
                if not grid.is_obstacle(nr, nc) and (nr, nc) not in visited:
                    new_g = g + 1
                    new_f = new_g + h((nr, nc), goal)
                    counter += 1
                    heapq.heappush(open_set, (new_f, counter, new_g, (nr, nc), path + [(nr, nc)]))

    return None
