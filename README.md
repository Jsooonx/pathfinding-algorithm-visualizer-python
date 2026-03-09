# Maze Pathfinding Algorithm Visualizer

A Python project that visualizes and compares pathfinding algorithms on grid-based mazes using Pygame.

## Features
- Visualizes how algorithms explore a maze step-by-step
- Compares three algorithms: DFS, BFS, and A*
- Highlights visited nodes and the final path
- Displays statistics (nodes explored and path length)
- Automatically cycles through all algorithms
- Supports custom mazes via `input.py`
- Includes multiple sample mazes with different difficulty levels

## Algorithms
- **DFS (Depth-First Search)** = explores one path deeply before backtracking
- **BFS (Breadth-First Search)** = explores level by level and guarantees the shortest path in an unweighted grid
- **A\*** = uses a heuristic (Manhattan distance) to guide the search toward the goal

## Project Structure
maze-pathfinding-visualizer/
- main.py = visualization and animation
- solver.py = DFS, BFS, and A* implementations
- input.py = maze configuration (maze, start, end)
- maze_samples.txt = sample mazes for testing

## Requirements
Python
pygame

Install pygame:
pip install pygame

## Run
python main.py

## Maze Format
0 = walkable path  
1 = wall

Example:
```
maze = [
[0,0,1,0],
[0,0,1,0],
[1,0,0,0],
[1,1,1,0]
]

start = (0,0)  
end = (3,3)
```

## Output
![Maze Visualizer Demo](assets/demo.png)

## Purpose
This project demonstrates basic graph traversal and heuristic search while providing a simple visual comparison between DFS, BFS, and A*.
