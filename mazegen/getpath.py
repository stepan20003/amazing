from collections import deque
from mazegen.mazemaze import MazeGen, MazeError
from typing import Any


class PathFinder(MazeGen):
    """
Maze solver and algorithm selector built on top of MazeGen.

This class extends MazeGen and is responsible for generating the maze
using the selected algorithm (DFS or Prim), and computing the shortest
path between entry and exit using Breadth-First Search (BFS).

It acts as a bridge between maze generation and pathfinding logic.

Attributes:
    maze (list[list[int]]): Generated maze grid.
    entry (tuple[int, int]): Entry coordinates.
    exit (tuple[int, int]): Exit coordinates.
"""
    def __init__(self, conf: dict[Any, Any]) -> None:
        super().__init__(conf)
        if conf['ALGORITM'] == 'dfs':
            self.maze = super().DFS_mazegen()
        else:
            self.maze = super().prim_generate()

    def find_short_path(self) -> list[tuple[int, int]]:
        """
Finds the shortest path between entry and exit using BFS.

The algorithm performs a breadth-first search over the maze grid,
respecting wall constraints encoded in each cell using bitmasks.
It reconstructs the shortest path using a parent-pointer dictionary.

Returns:
    list[tuple[int, int]]: Shortest path from entry to exit.

Raises:
    MazeError: If no valid path exists between entry and exit.
"""
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
                curr: tuple[int, int] | None = exit_room
                while curr is not None:
                    path.append((curr[1], curr[0]))
                    curr = ptogo[curr]
                return path[::-1]

            raw_cell = self.maze[cur_r][cur_c]
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
