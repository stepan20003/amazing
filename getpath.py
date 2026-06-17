from collections import deque
from mazemaze import MazeGen, MazeError
from typing import Any


class PathFinder(MazeGen):
    def __init__(self, conf: dict[Any, Any]):
        super().__init__(conf)

    def find_short_path(self):
        maze = super().mazegen()
        entry_room = (self.entry[1], self.entry[0])
        exit_room = (self.exit[1], self.exit[0])
        queue: deque[tuple[int, int]] = deque([entry_room])
        visited: set[tuple[int, int]] = {entry_room}
        ptogo: dict[
            tuple[int, int], tuple[int, int] | None] = {entry_room: None}
        direct = [
            (-1, 0, 1),
            (0, 1, 2),
            (1, 0, 4),
            (0, -1, 8)
        ]
        while queue:
            cur_r, cur_c = queue.popleft()
            if (cur_r, cur_c) == exit_room:
                path: list[tuple[int, int]] = []
                curr = exit_room
                while curr is not None:
                    path.append((curr[1], curr[0]))
                    curr = ptogo[curr]
                return path[::-1]

            raw_cell = maze[cur_r][cur_c]
            curr_cell = int(
                raw_cell, 16) if isinstance(raw_cell, str) else raw_cell
            for dx, dy, mask in direct:
                nr, nc = cur_r + dx, cur_c + dy
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if (curr_cell & mask) == 0:
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            ptogo[(nr, nc)] = (cur_r, cur_c)
                            queue.append((nr, nc))
        raise MazeError("Error: Path is not found")
