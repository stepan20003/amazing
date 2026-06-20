import matplotlib.pyplot as plt


def visualize(maze, path, start, end):
    h = len(maze)
    w = len(maze[0])

    fig, ax = plt.subplots(figsize=(w, h))

    ax.set_facecolor("white")

    # պատեր
    for y in range(h):
        for x in range(w):
            cell = maze[y][x]

            if cell & 1:  # North
                ax.plot([x, x+1], [h-y, h-y], "k")

            if cell & 2:  # East
                ax.plot([x+1, x+1], [h-y-1, h-y], "k")

            if cell & 4:  # South
                ax.plot([x, x+1], [h-y-1, h-y-1], "k")

            if cell & 8:  # West
                ax.plot([x, x], [h-y-1, h-y], "k")

    # shortest path
    px = [x + 0.5 for x, y in path]
    py = [h - y - 0.5 for x, y in path]

    ax.plot(px, py, linewidth=4)

    # Start
    ax.scatter(
        start[0] + 0.5,
        h - start[1] - 0.5,
        s=200,
        marker="o"
    )

    # Exit
    ax.scatter(
        end[0] + 0.5,
        h - end[1] - 0.5,
        s=200,
        marker="X"
    )

    ax.set_aspect("equal")
    ax.axis("off")

    plt.savefig("maze.png", bbox_inches="tight")
    plt.show()