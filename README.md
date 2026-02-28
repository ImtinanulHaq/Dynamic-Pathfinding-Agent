# Dynamic Pathfinding Agent

A Python-based dynamic pathfinding agent with a GUI that uses A* and Greedy Best-First Search algorithms to find paths on a grid with obstacles.

## Project Structure

```
Dynamic-Pathfinding-Agent/
├── main.py                  (entry point)
├── grid/
│   ├── grid.py              (Grid class with start, goal, obstacles)
│   ├── map_generator.py     (random obstacle generation)
│   └── editor.py            (toggle obstacles on/off)
├── algorithms/
│   ├── heuristics.py        (Manhattan and Euclidean heuristics)
│   ├── astar/
│   │   └── astar.py         (A* search algorithm)
│   └── gbfs/
│       └── gbfs.py          (Greedy Best-First Search)
├── agent/
│   └── agent.py             (Agent with position and movement)
├── gui/
│   └── gui.py               (Tkinter GUI with controls and visualization)
├── metrics/
│   └── metrics.py           (tracks nodes visited, path cost, time)
└── requirements.txt
```

## How to Run

```bash
python3 main.py
```

Make sure `python3-tk` is installed:

```bash
sudo apt install python3-tk
```

## Features

- **Grid**: Dynamic grid with adjustable size, start (orange), goal (green), obstacles (black)
- **Algorithms**: A* and Greedy Best-First Search (GBFS)
- **Heuristics**: Manhattan distance and Euclidean distance
- **Interactive GUI**: Click cells to add/remove obstacles
- **Dynamic Obstacles**: Random obstacles appear during agent movement, agent re-plans automatically
- **Metrics Dashboard**: Shows nodes visited, path cost, and execution time
- **Reset Button**: Clears the grid and starts fresh

## GUI Controls

- **Algorithm dropdown**: Choose between A* and GBFS
- **Heuristic dropdown**: Choose between Manhattan and Euclidean
- **Dynamic Obstacles checkbox**: Enable random obstacles during path animation
- **Run button**: Find and display the path
- **Reset button**: Clear everything and regenerate
- **Click on grid**: Add or remove obstacles

## Color Guide

| Color  | Meaning     |
|--------|-------------|
| Orange | Start point |
| Green  | Goal point  |
| Black  | Obstacle    |
| Yellow | Path found  |
| White  | Empty cell  |
