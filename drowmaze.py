from getpath import PathFinder
from sys import exit
from typing import Any
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("No dependencies installed use", end=" ")
    print("pip install -r requirements.txt")
    exit()


class DrowMaze(PathFinder):
    def __init__(self, conf: dict[Any, Any]):
        super().__init__(conf)
        self.road = self.find_short_path()

    def visual(self):
        h = self.height
        _, ax = plt.subplots(figsize=(self.width, h))
        ax.set_facecolor("white")
        for y in range(h):
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell & 1:
                    ax.plot([x, x+1], [h-y, h-y], "k")
                if cell & 2:
                    ax.plot([x+1, x+1], [h-y-1, h-y], "k")
                if cell & 4:
                    ax.plot([x, x+1], [h-y-1, h-y-1], "k")
                if cell & 8:
                    ax.plot([x, x], [h-y-1, h-y], "k")
        px = [x + 0.5 for x, _ in self.road]
        py = [h - y - 0.5 for _, y in self.road]
        ax.plot(px, py, linewidth=4)
        ax.scatter(
            self.entry[0] + 0.5,
            h - self.entry[1] - 0.5,
            s=200,
            marker="o"
        )
        ax.scatter(
            self.exit[0] + 0.5,
            h - self.exit[1] - 0.5,
            s=200,
            marker="X"
        )
        ax.set_aspect("equal")
        ax.axis("off")
        plt.savefig("maze.png", bbox_inches="tight")
        plt.show()
        exit()
