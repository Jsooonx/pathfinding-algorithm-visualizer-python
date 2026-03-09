import pygame
import sys
from solver import dfs, bfs, astar

# 0 = Walkable path
# 1 = Wall
maze = [
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
]

# Start and goal positions (row, col)
start = (0, 0)
end = (6, 6)

# Initialized pygame
pygame.init()

# Size of each grid
CELL_SIZE = 60

# Dimensions
ROWS = len(maze)
COLS = len(maze[0])

INFO_HEIGHT = 100

# Window dimensions
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + INFO_HEIGHT

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

# Fonts
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (220, 50, 50)
PURPLE = (150, 80, 200)
GRAY = (200, 200, 200)
BLUE = (100, 180, 255)
GREEN = (80, 200, 120)

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

# Run selected solver
def run_solver():
    global visit_order, path, step_index, show_path
    
    algorithm = algorithms[current_algorithm_index]
    
    if algorithm == "dfs":
        visit_order, path = dfs(maze, start, end)
    elif algorithm == "bfs":
        visit_order, path = bfs(maze, start, end)
    else:
        visit_order, path = astar(maze, start, end)
        
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

# Draw current algorightm info
def draw_info():
    algorithm = algorithms[current_algorithm_index]
    
    info_y = ROWS * CELL_SIZE + 10
    
    # Current algorithm label
    title_text = font.render(f"Algorithm: {algorithm.upper()}", True, BLACK)
    
    # Comparison stats
    nodes_text = small_font.render(f"Nodes explored: {len(visit_order)}", True, BLACK)
    path_text = small_font.render(f"Path length: {len(path)}", True, BLACK)
    
    screen.blit(title_text, (10, info_y))
    screen.bilt(nodes_text, (10, info_y + 35))
    screen.blit(path_text, (220, info_y + 35))
    
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
        pygame.display.flip()
        # Animation speed
        clock.tick(8)

# Run program
if __name__ == "__main__":
    main()