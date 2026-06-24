from typing import Any

from getpath import PathFinder


class DrowMaze(PathFinder):
    def __init__(self, conf: dict[str, Any]) -> None:
        self.road: list[tuple[int, int]] = []
        self.colors = [
            ("\033[0m██\033[0m", "\033[44m  \033[0m", "\033[45m  \033[0m",
             "\033[41m  \033[0m", "\033[100m  \033[0m", "\033[93m██\033[0m"),
            ("\033[32m██\033[0m", "\033[43m  \033[0m", "\033[45m  \033[0m",
             "\033[41m  \033[0m", "\033[47m  \033[0m", "\033[35m██\033[0m"),
            ("\033[31m██\033[0m", "\033[46m  \033[0m", "\033[42m  \033[0m",
             "\033[45m  \033[0m", "\033[100m  \033[0m", "\033[36m██\033[0m"),
            ("\033[33m██\033[0m", "\033[45m  \033[0m", "\033[42m  \033[0m",
             "\033[41m  \033[0m", "\033[100m  \033[0m", "\033[34m██\033[0m")
        ]
        self.color_index = 2
        super().__init__(conf)
        self.road = self.find_short_path()

    def rotate_colors(self) -> None:
        self.color_index = (self.color_index + 1) % len(self.colors)

    def build_terminal_map(self, show_path: bool = True) -> str:
        h = self.height
        w = self.width
        grid = self.maze
        path = self.road

        term_height = h * 3
        term_width = w * 3
        term_map = [["█" for _ in range(term_width)]
                    for _ in range(term_height)]
        (WALL_COLOR,
         BLUE,
         GREEN,
         RED,
         PATTERN_COLOR,
         WALL_42_COLOR) = self.colors[self.color_index]
        EMPTY = "  "
        for y in range(h):
            for x in range(w):
                val = grid[y][x]
                cx, cy = x * 3 + 1, y * 3 + 1
                is_42 = hasattr(self,
                                'pattern_42') and (x, y) in self.pattern_42
                if is_42:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            term_map[cy+dy][cx+dx] = "▓"
                if (x, y) == self.entry:
                    center_char = GREEN
                elif (x, y) == self.exit:
                    center_char = RED
                elif show_path and (x, y) in path:
                    center_char = BLUE
                elif is_42:
                    center_char = PATTERN_COLOR
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
                                                  and (x, y)
                                                  in path
                                                  and (x, y+1)
                                                  in path) else EMPTY
                if (val & 8) == 0:
                    term_map[cy][cx-1] = BLUE if (show_path
                                                  and (x, y)
                                                  in path
                                                  and (x-1, y)
                                                  in path) else EMPTY
        final_output = []
        for row in term_map:
            line_chars = []
            for char in row:
                if char == "█":
                    line_chars.append(WALL_COLOR)
                elif char == "▓":
                    line_chars.append(WALL_42_COLOR)
                else:
                    line_chars.append(char)
            final_output.append("".join(line_chars))
        return "\n".join(final_output)
