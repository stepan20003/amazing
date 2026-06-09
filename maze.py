import random
from writefile import masewrite


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


DIRECTIONS = {
    NORTH: (-1, 0, SOUTH),
    EAST:  (1, 0, WEST),
    SOUTH: (0, 1, NORTH),
    WEST:  (-1, 0, EAST)
}


def generate_maze_iterative(width: int, height: int, seed: int = None):
    if seed is not None:
        random.seed(seed)

    grid = [[15 for _ in range(width)] for _ in range(height)]

    start_x, start_y = 0, 0
    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}

    while stack:
        cx, cy = stack[-1]
        unvisited_neighbors = []

        for wall_bit, (dx, dy, opposite_bit) in DIRECTIONS.items():
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < width and 0 <= ny < height
               and (nx, ny) not in visited):
                unvisited_neighbors.append((nx, ny, wall_bit, opposite_bit))

        if unvisited_neighbors:
            nx, ny, wall_bit, opposite_bit = random.choice(unvisited_neighbors)
            grid[cy][cx] &= ~wall_bit
            grid[ny][nx] &= ~opposite_bit
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
    return grid


masewrite(generate_maze_iterative(15, 20))
