import random
from typing import Any


class MazeError(Exception):
    def __init__(self, m="Error: Maze size too small to fit the '42'"
                         "pattern. Minimum size is 7x5.") -> None:
        super().__init__(m)


class MazeGen:
    def __init__(
            self, conf: dict[Any, Any]) -> None:
        self.NORTH = 1
        self.EAST = 2
        self.SOUTH = 4
        self.WEST = 8

        self.MOVES: dict[int, tuple[int, int, int]] = {
            self.NORTH: (0, -1, self.SOUTH),
            self.EAST: (1, 0, self.WEST),
            self.SOUTH: (0, 1, self.NORTH),
            self.WEST: (-1, 0, self.EAST)
        }

        self.PAT42: list[list[int]] = [
                [1, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1]
        ]

        self.width = conf["WIDTH"]
        self.height = conf["HEIGHT"]
        self.entry = conf["ENTRY"]
        self.exit = conf["EXIT"]
        self.seed = conf["SEED"]

    def mazegen(self) -> list[list[int]]:
        """Gen maze and open doors"""
        stack: list[tuple[int, int]] = []
        if self.seed is not None:
            random.seed(self.seed)

        grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        visited = set()
        start_pat_x = (self.width - 7) // 2
        start_pat_y = (self.height - 5) // 2
        if self.width >= 7 and self.height >= 5:
            for py in range(5):
                for px in range(7):
                    if self.PAT42[py][px] == 1:
                        mazx = start_pat_x + px
                        mazy = start_pat_y + py
                        visited.add((mazx, mazy))
        else:
            print("Maze size too small to fit the '42'", end=" ")
            print("pattern. Minimum size for patern is 7x5.")
        if self.entry in list(visited) or self.exit in list(visited):
            raise MazeError("Entry or Exit points in 42 patern")
        stack.append(self.entry)
        visited.add(self.entry)
        while stack:
            cx, cy = stack[-1]
            unvis_neighbors = []
            for move_to, (mx, my, br_wall) in self.MOVES.items():
                nx, ny = cx + mx, cy + my
                if (0 <= nx < self.width and 0 <= ny < self.height and
                   (nx, ny) not in visited):
                    unvis_neighbors.append((nx, ny, move_to, br_wall))
            if unvis_neighbors:
                nx, ny, move_to, br_wall = random.choice(unvis_neighbors)
                grid[cy][cx] &= ~move_to
                grid[ny][nx] &= ~br_wall
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        return grid
