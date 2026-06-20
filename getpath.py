from collections import deque
from mazemaze import MazeGen, MazeError
from typing import Any


class PathFinder(MazeGen):
    def __init__(self, conf: dict[Any, Any]):
        super().__init__(conf)

    def find_short_path(self):
        maze = self.grid
        entry_room = self.entry  # (x, y)
        exit_room = self.exit    # (x, y)
        queue: deque[tuple[int, int]] = deque([entry_room])
        visited: set[tuple[int, int]] = {entry_room}
        ptogo: dict[tuple[int, int], tuple[int, int] | None] = {entry_room: None}
        direct = [
                (0, -1, 1, 4),   # N (հակառակը՝ S = 4)
                (1, 0, 2, 8),    # E (հակառակը՝ W = 8)
                (0, 1, 4, 1),    # S (հակառակը՝ N = 1)
                (-1, 0, 8, 2)    # W (հակառակը՝ E = 2)
        ]

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == exit_room:
                path: list[tuple[int, int]] = []
                curr = exit_room
                while curr is not None:
                    path.append(curr)
                    curr = ptogo[curr]
                return path[::-1]

            curr_cell = maze[cy][cx]

            for dx, dy, mask, rev_mask in direct:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    next_cell = maze[ny][nx]

        # Ստուգում ենք՝ արդյոք ընթացիկ բջջից ելքը բաց է 
        # ԵՎ հարևան բջջից մուտքը նույնպես բաց է
                    if (curr_cell & mask) == 0 and (next_cell & rev_mask) == 0:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            ptogo[(nx, ny)] = (cx, cy)
                            queue.append((nx, ny))

        raise MazeError("Error: Path is not found")
        
    