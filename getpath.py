from collections import deque
from confvalidator import filldict


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

MOVES = {
    NORTH: (0, -1),
    EAST:  (1, 0),
    SOUTH: (0, 1),
    WEST:  (-1, 0)
}


def solve_maze(grid, start, end):
    h = len(grid)
    w = len(grid[0])

    queue = deque([start])
    visited = set([start])

    parent = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            break

        cell = grid[y][x]

        for direction, (dx, dy) in MOVES.items():

            if not (cell & direction):
                nx, ny = x + dx, y + dy

                if 0 <= nx < w and 0 <= ny < h:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)

    if end not in parent and start != end:
        return None

    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()

    return path


def path_to_dirs(path):
    dirs = []

    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]

        dx = x2 - x1
        dy = y2 - y1

        if dx == -1 and dy == 0:
            dirs.append("W")
        elif dx == 1 and dy == 0:
            dirs.append("E")
        elif dx == 0 and dy == 1:
            dirs.append("S")
        elif dx == 0 and dy == -1:
            dirs.append("N")

    return dirs


def solving():
    with open("maze.txt", "r") as f:
        path = f.read()
        path = path.split("\n")
        result = [[int(c, 16) for c in i] for i in path]
    conf = filldict()

    x = solve_maze(result, conf["ENTRY"], conf["EXIT"])
    print(*path_to_dirs(x))

solving()
