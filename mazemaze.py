import random
import sys
from typing import Any


class MazeError(Exception):
    def __init__(
        self,
        m: str = (
            "Error: Maze size too small to fit the '42' "
            "pattern. Minimum size is 7x5."
        ),
    ) -> None:
        super().__init__(m)


class MazeGen:
    def __init__(
            self, conf: dict[Any, Any]) -> None:
        self.conf = conf
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

    def start_animation(self) -> None:
        pass

    def draw_animation_frame(self, delay: float = 0.03) -> None:
        pass

    def mazegen(self) -> list[list[int]]:
        stack: list[tuple[int, int]] = []
        animate = sys.stdout.isatty()
        if animate:
            self.start_animation()
        if self.seed is not None:
            random.seed(self.seed)
        grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.maze = grid
        visited = set()
        self.pattern_42 = set()
        start_pat_x = (self.width - 7) // 2
        start_pat_y = (self.height - 5) // 2
        if self.width >= 7 and self.height >= 5:
            for py in range(5):
                for px in range(7):
                    if self.PAT42[py][px] == 1:
                        mazx = start_pat_x + px
                        mazy = start_pat_y + py
                        visited.add((mazx, mazy))
                        self.pattern_42.add((mazx, mazy))
        else:
            raise MazeError()
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
                if animate:
                    self.draw_animation_frame()
            else:
                stack.pop()

        if not self.conf['PERFECT']:
            dead_ends = []
            for cy in range(1, self.height - 1):
                for cx in range(1, self.width - 1):
                    if (cx, cy) in self.pattern_42:
                        continue
                    if bin(grid[cy][cx]).count('1') == 3:
                        dead_ends.append((cx, cy))
            random.shuffle(dead_ends)
            for cx, cy in dead_ends[:len(dead_ends) // 2]:
                valid_moves = []
                for move_to, (mx, my, br_wall) in self.MOVES.items():
                    nx, ny = cx + mx, cy + my
                    if (0 < nx < self.width - 1 and 0 < ny < self.height - 1
                            and (nx, ny) not in self.pattern_42):
                        if grid[cy][cx] & move_to:
                            valid_moves.append((nx, ny, move_to, br_wall))
                if valid_moves:
                    nx, ny, move_to, br_wall = random.choice(valid_moves)
                    grid[cy][cx] &= ~move_to
                    grid[ny][nx] &= ~br_wall
                    if animate:
                        self.draw_animation_frame()
        return grid
