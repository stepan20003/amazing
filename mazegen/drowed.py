import sys
import time
from typing import Any
from mazegen.getpath import PathFinder


class DrowMaze(PathFinder):
    """
Terminal-based animated maze renderer with path visualization.

This class extends PathFinder and provides an interactive terminal UI
for displaying generated mazes. It supports colored rendering, animated
generation, shortest path visualization, and dynamic updates.

Features:
    - ANSI terminal rendering of maze grid
    - Animated maze solving/path drawing
    - Multiple color themes
    - Toggleable shortest path display
    - Support for special "42 pattern" overlay

Attributes:
    road (list[tuple[int, int]]): Computed shortest path.
    colors (list[tuple[str, ...]]): Available rendering color themes.
    color_index (int): Current active color theme index.
    animate (int): Animation mode flag (1 = enabled, 0 = disabled).
    _frame_line_count (int): Internal tracking of rendered terminal lines.
"""
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
        self.animate = 1
        self._frame_line_count = 0
        super().__init__(conf)
        self.road = self.find_short_path()
        if self.animate:
            self.finish_animation(self.build_terminal_map(show_path=True))
        else:
            print(self.build_terminal_map(show_path=False))

    def find_short_path(self) -> list[tuple[int, int]]:
        """
Computes and animates the shortest path in the maze.

Calls the parent PathFinder implementation to compute the shortest path,
then progressively visualizes it step-by-step in the terminal if animation
is enabled.

Returns:
    list[tuple[int, int]]: The shortest path from entry to exit.
"""
        path = super().find_short_path()
        if not self.animate:
            return path
        self.road = []
        for step in range(1, len(path) + 1):
            self.road = path[:step]
            if self.animate == 1:
                self.draw_path_frame()
        return path

    def _refresh_terminal(
            self, content: str, *, clear_screen: bool = False) -> None:
        """
Updates the terminal display with new frame content.

Handles cursor positioning, screen clearing, and efficient line-by-line
redrawing for smooth animation.

Args:
    content (str): The rendered maze frame to display.
    clear_screen (bool): Whether to clear the screen before rendering.

Returns:
    None
"""
        if not self.animate:
            return
        if clear_screen:
            sys.stdout.write("\033[2J\033[H")
        lines = content.split("\n") if content else []
        for row, line in enumerate(lines, start=1):
            sys.stdout.write(f"\033[{row};1H\033[2K{line}")
        for row in range(len(lines) + 1, self._frame_line_count + 1):
            sys.stdout.write(f"\033[{row};1H\033[2K")
        self._frame_line_count = len(lines)
        sys.stdout.flush()

    def start_animation(self) -> None:
        """
Initializes terminal animation mode.

Switches to an alternate terminal buffer, hides cursor,
and prepares screen for animated rendering.

Returns:
    None
"""
        if not self.animate:
            return
        sys.stdout.write("\033[?1049h\033[?25l\033[2J\033[H")
        sys.stdout.flush()
        self._frame_line_count = 0

    def finish_animation(self, content: str) -> None:
        """
Terminates animation mode and restores terminal state.

Restores normal terminal buffer and cursor visibility, then
renders the final maze frame.

Args:
    content (str): Final frame to display.

Returns:
    None
"""
        if not self.animate:
            return
        sys.stdout.write("\033[?1049l\033[?25h")
        sys.stdout.flush()
        self._frame_line_count = 0
        self._refresh_terminal(content, clear_screen=True)

    def draw_animation_frame(self, delay: float = 0.03) -> None:
        """
Renders a single frame of maze generation animation.

Displays the current maze state without the solution path,
optionally delaying execution for visualization.

Args:
    delay (float): Time delay between frames in seconds.

Returns:
    None
"""
        if self.animate == 1:
            self._refresh_terminal(self.build_terminal_map(show_path=False))
            time.sleep(delay)
        else:
            delay = 0
            self._refresh_terminal(self.build_terminal_map(show_path=False))
            time.sleep(delay)

    def draw_path_frame(self, delay: float = 0.06) -> None:
        """
Renders a single frame of shortest path animation.

Displays the maze with the currently revealed path step,
used to animate path discovery.

Args:
    delay (float): Time delay between frames in seconds.

Returns:
    None
"""
        if self.animate == 1:
            self._refresh_terminal(self.build_terminal_map(show_path=True))
            time.sleep(delay)
        else:
            delay = 0
            self._refresh_terminal(self.build_terminal_map(show_path=True))
            time.sleep(delay)

    def rotate_colors(self) -> None:
        """
Cycles to the next available color theme.

Updates the active terminal rendering palette used for maze display.

Returns:
    None
"""
        self.color_index = (self.color_index + 1) % len(self.colors)

    def build_terminal_map(self, show_path: bool = True) -> str:
        """
Builds a full ASCII/ANSI representation of the maze for terminal display.

Converts the internal maze grid into a colored 2D terminal representation,
including walls, entry/exit points, shortest path (optional), and
special "42 pattern" visualization.

Args:
    show_path (bool): Whether to display the shortest path.

Returns:
    str: Fully rendered terminal string representation of the maze.
"""
        h = self.height
        w = self.width
        grid = self.maze
        path = self.road

        term_height = h * 3
        term_width = w * 3
        term_map = [["#" for _ in range(term_width)]
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
                is_42 = (x, y) in self.pattern_42
                if is_42:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            term_map[cy+dy][cx+dx] = "+"
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
                if char == "#":
                    line_chars.append(WALL_COLOR)
                elif char == "+":
                    line_chars.append(WALL_42_COLOR)
                else:
                    line_chars.append(char)
            final_output.append("".join(line_chars))
        return "\n".join(final_output)
