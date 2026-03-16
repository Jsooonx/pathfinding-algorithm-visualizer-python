import pygame
import sys
from solver import dfs, bfs, astar
from input import maze, start, end
from config import (
    CELL_SIZE,
    INFO_HEIGHT,
    FPS,
    PAUSE_FRAMES,
    WHITE,
    BLACK,
    RED,
    PURPLE,
    GRAY,
    BLUE,
    GREEN,
    YELLOW,
    ALGORITHMS,
)

def validate_input(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])

    # Check maze is not empty
    if rows == 0 or cols == 0:
        raise ValueError("Maze cannot be empty.")

    # Check all rows have same length
    for row in maze:
        if len(row) != cols:
            raise ValueError("All rows in the maze must have the same length.")

    # Check start and end are inside the maze
    for position, name in [(start, "start"), (end, "end")]:
        r, c = position
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{name.capitalize()} position is out of bounds.")

        if maze[r][c] != 0:
            raise ValueError(f"{name.capitalize()} position must be on a walkable cell.")
        
validate_input(maze, start, end)

# Initialized pygame
pygame.init()

# Size of each grid
CELL_SIZE = 60

# Dimensions
ROWS = len(maze)
COLS = len(maze[0])

INFO_HEIGHT = 170

# Window dimensions
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + INFO_HEIGHT

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

# Fonts
font = pygame.font.Font("assets/PlayfairDisplay-Regular.ttf", 26)
small_font = pygame.font.Font("assets/PlayfairDisplay-Regular.ttf", 18)

# Clock controls animation speed
clock = pygame.time.Clock()

# List of algo
algorithms = ["dfs", "bfs", "astar"]

current_algorithm_index = 0

# Animation state
visit_order = []
path = []
step_index = 0
show_path = False
pause_counter = 0

PAUSE_FRAMES = 30

def get_all_results():
    results = {}
    
    for algorithm in algorithms:
        if algorithm == "dfs":
            current_visit_order, current_path = dfs(maze, start, end)
        elif algorithm == "bfs":
            current_visit_order, current_path = bfs(maze, start, end)
        else:
            current_visit_order, current_path = astar(maze, start, end)
            
        results[algorithm] = {
            "visit_order": current_visit_order,
            "path": current_path,
            "nodes_explored": len(current_visit_order),
            "path_length": len(current_path)
        }
    
    return results

# Store comparison results
results = get_all_results()

def run_solver():
    global visit_order, path, step_index, show_path

    algorithm = algorithms[current_algorithm_index]

    visit_order = results[algorithm]["visit_order"]
    path = results[algorithm]["path"]

    # Reset animation
    step_index = 0
    show_path = False
    
# Draw maze grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            
            # Convert grid coordinate to screen coordinate
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            
            # Choose color depending on wall or path
            if maze[row][col] == 1:
                color = BLACK
            else:
                color = WHITE
                
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Draw visited nodes
def draw_visited():
    
    # Only draw nodes explored so far
    for row, col in visit_order[:step_index]:
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, GRAY, rect, 1)


# Draw final path
def draw_path():
    
    for row, col in path:
        
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, GRAY, rect, 1)

# Draw start and end nodes
def draw_start_end():
    sr, sc = start
    er, ec = end
    
    # Start node
    pygame.draw.rect(screen, RED, (sc * CELL_SIZE, sr * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Goal node
    pygame.draw.rect(screen, PURPLE, (ec * CELL_SIZE, er * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw current algorithm info
def draw_info():
    algorithm = algorithms[current_algorithm_index]
    
    info_y = ROWS * CELL_SIZE + 10
    
    # Current algorithm label
    title_text = font.render(f"Algorithm: {algorithm.upper()}", True, BLACK)
    
    # Comparison stats
    nodes_text = small_font.render(f"Nodes explored: {len(visit_order)}", True, BLACK)
    path_text = small_font.render(f"Path length: {len(path)}", True, BLACK)
    
    screen.blit(title_text, (10, info_y))
    screen.blit(nodes_text, (10, info_y + 35))
    screen.blit(path_text, (220, info_y + 35))
    
# Draw comparison summary
def draw_summary():
    summary_y = ROWS * CELL_SIZE + 80
    current_algorithm = algorithms[current_algorithm_index]

    # Summary title
    summary_title = small_font.render("Comparison Summary", True, BLACK)
    screen.blit(summary_title, (10, summary_y))

    # Summary rows
    summary_rows = [
        ("dfs", f"DFS  - Nodes: {results['dfs']['nodes_explored']}  Path: {results['dfs']['path_length']}"),
        ("bfs", f"BFS  - Nodes: {results['bfs']['nodes_explored']}  Path: {results['bfs']['path_length']}"),
        ("astar", f"A*  - Nodes: {results['astar']['nodes_explored']}  Path: {results['astar']['path_length']}")
    ]

    for index, (name, text) in enumerate(summary_rows):
        y = summary_y + 30 + (index * 25)

        # Highlight the algorithm currently being animated
        if name == current_algorithm:
            highlight_rect = pygame.Rect(8, y + 2, 300, 22)
            pygame.draw.rect(screen, YELLOW, highlight_rect, border_radius=6)

        row_text = small_font.render(text, True, BLACK)
        screen.blit(row_text, (10, y))

# Move to next algorithm
def next_algorithm():
    global current_algorithm_index, pause_counter
    
    current_algorithm_index = (current_algorithm_index + 1) % len(algorithms)
    pause_counter = 0
    run_solver()
    
# Main program loop
def main():
    global step_index, show_path, pause_counter
    
    # Run first algorithm
    run_solver()
    
    while True:
        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Animation logic
        if step_index < len(visit_order):
            step_index += 1
        else:
            show_path = True
            
            # Pause for a moment
            if pause_counter < PAUSE_FRAMES:
                pause_counter += 1
            else:
                next_algorithm()
        
        # Draw everything
        screen.fill(WHITE)
        draw_grid()
        draw_visited()
        
        if show_path:
            draw_path()
            
        draw_start_end()
        draw_info()
        draw_summary()
        
        pygame.display.flip()
        # Animation speed
        clock.tick(8)

# Run program
if __name__ == "__main__":
    main()