from collections import deque
import heapq

# Get valid neighboring cells
def get_neighbors(position, maze):
    row, col = position
    neighbors = []
    
    # Possible movement directions: up, down, left, right
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    
    rows = len(maze)
    cols = len(maze[0])
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Check whether the new position is still inside the grid
        if 0 <= new_row < rows and 0 <= new_col < cols:
            
            # Check whether the cell is walkable
            if maze[new_row][new_col] == 0:
                neighbors.append((new_row, new_col))
                
    return neighbors

# Reconstruct final path from end back to start
def reconstruct_path(parent, start, end):
    # Special case
    if start == end:
        return [start]
    
    # If end is not in parent, that means no path was found
    if end not in parent:
        return []
    
    path = []
    current = end
    
    # Trace backward
    while current != start:
        path.append(current)
        current = parent[current]
        
    # Add start node
    path.append(start)
    
    # Reverse so the path goes from start to end
    path.reverse()
    return path

# DFS
def dfs(maze, start, end):
    stack = [start]
    visited = set([start])
    parent = {}
    visit_order = []
    
    while stack:
        # Take the most recent added node
        current = stack.pop()
        visit_order.append(current)
        
        # Stop if goal is reached
        if current == end:
            path = reconstruct_path(parent, start, end)
            return visit_order, path
        
        # Explore neighbors
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
                
    # No path found
    return visit_order, []

# BFS
def bfs(maze, start, end):
    queue = deque([start])
    visited = set([start])
    parent = {}
    visit_order = []
    
    while queue:
        # Take the oldest added node
        current = queue.popleft()
        visit_order.append(current)
        
        # Stop if goal is reached
        if current == end:
            path = reconstruct_path(parent, start, end)
            return visit_order, path
        
        # Explore neighbors
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                
    # No path found
    return visit_order, []

# Heuristic for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* search
def astar (maze, start, end):
    # Priority queue
    heap = []
    heapq.heappush(heap, (0, start))
    
    parent = {}
    g_cost = {start: 0}
    visited = set()
    visit_order = []
    
    while heap:
        # Pop node with smallest priority
        _, current = heapq.heappop(heap)
        
        # Skip if already processed
        if current in visited:
            continue
        
        visited.add(current)
        visit_order.append(current)
        
        # Stop if goal is reached
        if current == end:
            path = reconstruct_path(parent, start, end)
            return visit_order, path
        
        # Explore neighbors
        for neighbor in get_neighbors(current, maze):
            tentative_g = g_cost[current] + 1
            
            # Update only if this path is better
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                parent[neighbor] = current
                
                f_cost = tentative_g + heuristic(neighbor, end)
                heapq.heappush(heap, (f_cost, neighbor))
                
    # No path found
    return visit_order, []