from writefile import masewrite
from confvalidator import filldict
import random


class MazeError(Exception):
    def __init__(self) -> None:
        m = "Error: Maze size too small to fit the '42'" \
            "pattern. Minimum size is 7x5."
        super().__init__(m)


class MazeGen:
    def __init__(
            self, conf: dict[str: str | int | None | tuple[int, int]]) -> None:
        self.NORTH = 1
        self.EAST = 2
        self.SOUTH = 4
        self.WEST = 8

        self.MOVES: dict[int: tuple[int, int, int]] = {
            self.NORTH: (0, -1, self.SOUTH),
            self.EAST: (1, 0, self.WEST),
            self.SOUTH: (0, 1, self.NORTH),
            self.WEST: (-1, 0, self.EAST)
        }

        self.PAT42 = [
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
        self.stack: list[int] = []
        self.visited = set()

    def mazegen(self) -> list[list[int]]:
        if self.seed is not None:
            random.seed(self.seed)

        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.stack.append(self.entry)
        self.visited.add(self.entry)
        start_pat_x = (self.width - 7) // 2
        start_pat_y = (self.height - 5) // 2
        if self.width >= 7 and self.height >= 5:
            for py in range(5):
                for px in range(7):
                    if self.PAT42[py][px] == 1:
                        mazx = start_pat_x + px
                        mazy = start_pat_y + py
                        self.visited.add((mazx, mazy))

        else:
            raise MazeError
        print(self.stack)
        while self.stack:
            cx, cy = self.stack[-1]
            unvis_neighbors = []
            for move_to, (mx, my, br_wall) in self.MOVES.items():
                nx, ny = cx + mx, cy + my
                if (0 <= nx < self.width and 0 <= ny < self.height and
                   (nx, ny) not in self.visited):
                    unvis_neighbors.append((nx, ny, move_to, br_wall))
            if unvis_neighbors:
                nx, ny, move_to, br_wall = random.choice(unvis_neighbors)
                self.grid[cy][cx] &= ~move_to
                self.grid[ny][nx] &= ~br_wall
                self.visited.add((nx, ny))
                self.stack.append((nx, ny))
            else:
                self.stack.pop()
        return self.grid


if __name__ == "__main__":
    maze = MazeGen(filldict())
    masewrite(maze.mazegen())
