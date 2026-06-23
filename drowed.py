from getpath import PathFinder
from typing import Any


class DrowMaze(PathFinder):
    def __init__(self, conf: dict[Any, Any]):
        super().__init__(conf)
        self.road = self.find_short_path()

    def build_terminal_map(self, show_path=True):
        h = self.height
        w = self.width
        grid = self.maze
        path = self.road

        term_height = h * 3
        term_width = w * 3
        term_map = [["█" for _ in range(term_width)]
                    for _ in range(term_height)]
        GREEN = "\033[42m  \033[0m"
        RED = "\033[41m  \033[0m"
        BLUE = "\033[44m  \033[0m"
        WALL = "██"
        EMPTY = "  "
        for y in range(h):
            for x in range(w):
                val = grid[y][x]
                cx, cy = x * 3 + 1, y * 3 + 1
                if (x, y) == self.entry:
                    center_char = GREEN
                elif (x, y) == exit:
                    center_char = RED
                elif show_path and (x, y) in path:
                    center_char = BLUE
                else:
                    center_char = EMPTY
                term_map[cy][cx] = center_char
                if (val & 1) == 0:
                    term_map[cy-1][cx] = BLUE if (show_path
                                                  and (x, y)
                                                  in path
                                                  and (x, y-1)
                                                  in path) else EMPTY
                if (val & 2) == 0:
                    term_map[cy][cx+1] = BLUE if (show_path
                                                  and (x, y)
                                                  in path
                                                  and (x+1, y)
                                                  in path) else EMPTY
                if (val & 4) == 0:
                    term_map[cy+1][cx] = BLUE if (show_path
                                                  and (x, y) in path
                                                  and (x, y+1)
                                                  in path) else EMPTY
                if (val & 8) == 0:
                    term_map[cy][cx-1] = BLUE if (show_path
                                                  and (x, y) in path
                                                  and (x-1, y)
                                                  in path) else EMPTY
        final_output = []
        for row in term_map:
            line_str = "".join([WALL if char == "█" else char for char in row])
            final_output.append(line_str)
        return "\n".join(final_output)
