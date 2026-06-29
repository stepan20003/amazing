*This project has been created as part of the 42 curriculum by rafhovha, ststepan.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator. Given a simple text configuration
file, it builds a grid-based maze, guarantees it is solvable from a defined
entry to a defined exit, embeds a visible "42" pattern made of fully closed
cells, and writes the result to a file using a compact hexadecimal wall
encoding. The maze is also rendered live in the terminal (ASCII), where the
shortest path, wall colours, and a brand-new maze can all be toggled
interactively.

The goal of the project is twofold:

- Apply graph theory and randomized algorithms (spanning trees, DFS,
  Prim's algorithm) to a concrete, visual problem.
- Produce a clean, reusable, type-checked Python module (`mazegen`) that can
  be installed with `pip` and reused in any future project that needs a
  maze.

## Features

- Two interchangeable generation algorithms: **recursive backtracker (DFS)**
  and **Prim's algorithm** (bonus — selectable via config).
- Perfect or imperfect maze generation (`PERFECT` flag).
- Deterministic generation via a `SEED` for reproducibility.
- Guaranteed: no 3x3+ open areas, no isolated cells, coherent shared walls
  between neighbouring cells, closed external borders except at entry/exit.
- A visible "42" shape drawn with fully closed cells, automatically skipped
  (with a warning) on mazes too small to fit it.
- Shortest path computed with a BFS solver and exported in `N`/`E`/`S`/`W`
  notation.
- ASCII terminal rendering with an interactive menu:
  - Re-generate a new maze.
  - Show / hide the shortest path.
  - Cycle through wall colours.
- A standalone, pip-installable `mazegen` package exposing the generation
  engine independently of the CLI tool.

## Instructions

### Requirements

- Python 3.10+
- `pip` (or `uv` / `pipx`)

### Installation

```bash
git clone <repo_url>
cd a-maze-ing
make install
```

`make install` creates/uses a virtual environment and installs the
dependencies listed in `requirements.txt` (and, if needed, the local
`mazegen` package in editable mode).

### Running the project

```bash
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` is the mandatory entry point name.
- `config.txt` is the configuration file (a default one is provided at the
  repository root). Any filename can be passed as long as it follows the
  expected format.

### Makefile targets

| Target        | Description                                               |
|---------------|-------------------------------------------------------------|
| `make install`      | Installs project dependencies.                        |
| `make run`          | Runs `python3 a_maze_ing.py config.txt`.               |
| `make debug`        | Runs the program under `pdb`.                          |
| `make clean`        | Removes `__pycache__`, `.mypy_cache`, build artifacts. |
| `make lint`         | Runs `flake8 .` and `mypy .` with the mandatory flags. |
| `make lint-strict`  | Runs `flake8 .` and `mypy . --strict`.                 |

### Building the reusable `mazegen` package

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install build
python3 -m build
```

This produces `mazegen-<version>-py3-none-any.whl` and
`mazegen-<version>.tar.gz` at the repository root, ready to be installed
with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are comments and are
ignored.

| Key             | Mandatory | Description                                  | Example                 |
|-----------------|-----------|-----------------------------------------------|--------------------------|
| `WIDTH`         | Yes       | Maze width, in cells                          | `WIDTH=20`               |
| `HEIGHT`        | Yes       | Maze height, in cells                         | `HEIGHT=15`              |
| `ENTRY`         | Yes       | Entry coordinates `x,y`                       | `ENTRY=0,0`              |
| `EXIT`          | Yes       | Exit coordinates `x,y`                        | `EXIT=19,14`             |
| `OUTPUT_FILE`   | Yes       | Path of the generated output file             | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`       | Yes       | `True`/`False` — exactly one path if true     | `PERFECT=True`           |
| `SEED`          | No        | Integer seed for reproducible generation      | `SEED=42`                |
| `ALGORITHM`     | No        | `dfs` or `prim` (default: `dfs`)              | `ALGORITHM=prim`         |
| `DISPLAY`       | No        | Reserved for future display modes             | `DISPLAY=ascii`          |

Example `config.txt`:

```
# Default maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=dfs
```

### Output file format

- One line per row, one hexadecimal digit per cell.
- Each digit's bits encode which walls are **closed**: bit 0 = North,
  bit 1 = East, bit 2 = South, bit 3 = West (a set bit means the wall is
  closed, a `0` bit means it is open).
- After an empty line: entry coordinates, exit coordinates, then the
  shortest path from entry to exit as a string of `N`/`E`/`S`/`W` letters.
- Every line ends with `\n`.

## Maze generation algorithm

Two algorithms are implemented behind a common interface, selectable via the
`ALGORITHM` key:

### Recursive backtracker (DFS) — default

Starting from the entry cell, the algorithm randomly visits an unvisited
neighbour, knocks down the wall between the current cell and that
neighbour, and recurses. When no unvisited neighbour remains, it backtracks
along the call stack (implemented with an explicit stack to avoid Python's
recursion limit on large mazes) until a cell with an unvisited neighbour is
found again.

### Prim's algorithm (bonus)

Starting from a single cell, the algorithm maintains a frontier of walls
adjacent to the growing maze. At each step, it picks a random wall from the
frontier; if it separates a cell already in the maze from a cell that isn't,
the wall is removed and the new cell's walls are added to the frontier.

### Why these two

- The **recursive backtracker** was chosen first because it directly
  produces a **perfect maze**: by construction, the set of removed walls
  forms a spanning tree of the grid graph, so there is exactly one path
  between any two cells — exactly what the `PERFECT` flag requires, with no
  extra post-processing.
- **Prim's algorithm** was added as a bonus because it produces a visibly
  different texture (shorter, more frequent dead ends rather than long
  winding corridors), which is a good illustration that several spanning
  tree algorithms solve the same graph problem with different statistical
  properties, while still guaranteeing a perfect maze.
- For non-perfect mazes (`PERFECT=False`), both algorithms first build a
  perfect maze, then a controlled number of extra walls are randomly removed
  (without ever creating a forbidden 3x3+ open area) to introduce loops.
- The "42" pattern and the open-area width constraint are enforced as a
  post-processing pass on top of either algorithm, keeping the generation
  core and the constraint-enforcement logic decoupled and testable
  independently.

## Reusable module — `mazegen`

The whole generation engine lives in `mazegen/`, independent from the CLI
script (`a_maze_ing.py`), and is published as a standalone, pip-installable
package (`mazegen-*.whl` / `mazegen-*.tar.gz` at the repository root).

What is reusable:

- `mazegen.MazeGenerator`: the class containing all generation logic
  (DFS and Prim's), validation rules, and the "42" pattern injector.
- `mazegen.solver.shortest_path`: a BFS-based solver usable on any
  `MazeGenerator` instance.
- Nothing in `mazegen` depends on the CLI, the config-file parser, or the
  ASCII renderer — those stay in `a_maze_ing.py`, so the package can be
  dropped into any other project that just needs maze data.

### Basic usage

```python
from mazegen import MazeGenerator

# Instantiate with custom parameters
maze = MazeGenerator(width=20, height=15, seed=42, algorithm="dfs")

# Generate the maze (perfect, with entry/exit)
maze.generate(entry=(0, 0), exit=(19, 14), perfect=True)

# Access the generated structure: a 2D list of Cell objects,
# each exposing .walls (a dict of N/E/S/W -> bool)
grid = maze.grid

# Access a solution (list of (x, y) coordinates, or N/E/S/W string)
path_cells = maze.shortest_path()
path_letters = maze.shortest_path_as_directions()
```

Passing custom parameters:

```python
maze = MazeGenerator(
    width=30,
    height=30,
    seed=1234,          # reproducibility
    algorithm="prim",   # "dfs" (default) or "prim"
)
```

This same documentation (instantiation, custom parameters, accessing the
structure and the solution) is also included inside the `mazegen` package
itself (its own `README.md` / module docstrings), as required.

## Resources

- *Mazes for Programmers* — Jamis Buck (recursive backtracker, Prim's,
  and other maze algorithms, with pseudocode).
- Wikipedia — [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm).
- Wikipedia — [Spanning tree](https://en.wikipedia.org/wiki/Spanning_tree) (link between perfect mazes and spanning trees).
- [PEP 257](https://peps.python.org/pep-0257/) — docstring conventions.
- [mypy documentation](https://mypy.readthedocs.io/) and [flake8 documentation](https://flake8.pycqa.org/) for the static-analysis setup.
- [Python Packaging User Guide](https://packaging.python.org/) — building the `mazegen` wheel/sdist.

### How AI was used

- Used to discuss the trade-offs between maze algorithms (DFS vs Prim's vs
  Kruskal's) before deciding which two to implement; the actual
  implementation and adaptation to our constraints (42 pattern, open-area
  limit, coherent shared walls) was written and reviewed by ourselves.
- Used to draft the initial Makefile lint/mypy flags so they matched the
  subject exactly, then verified manually against the subject and adjusted.
- Used to brainstorm edge cases to test (entry == exit, maze too small for
  "42", non-perfect maze with disconnected regions) — the corresponding
  tests were written and validated by us.
- Not used to generate the core maze-generation algorithms or the CLI logic
  directly; all generated suggestions were reviewed, discussed between the
  two of us, and rewritten where needed so both team members can fully
  explain every part of the code during defense.

## Team and project management

| Member     | Role                                                              |
|------------|---------------------------------------------------------------------|
| rafhovha   | Maze generation core (DFS & Prim's), wall-coherence & validation logic, "42" pattern injector. |
| ststepan   | Config parsing & error handling, ASCII renderer & interactive menu, BFS solver, `mazegen` packaging. |

Both authors reviewed and tested each other's modules together before
integration.

### Planning

We split the work into three phases: (1) core data structures and config
parsing, (2) the two generation algorithms plus validation constraints
(open areas, "42" pattern, perfect/imperfect), (3) the ASCII renderer,
solver, and packaging. The original estimate under-budgeted the time needed
to debug the wall-coherence checks between neighbouring cells and the "42"
placement on small mazes, so we shifted a day from the bonus (Prim's) phase
to hardening the mandatory part first, then came back to finish Prim's once
the mandatory part was fully validated and linted.

### What worked well / what could be improved

- Working well: splitting generation logic from CLI/I-O early made it easy
  to package `mazegen` independently and to write isolated tests for each
  algorithm.
- To improve: we underestimated how many edge cases the "42" pattern
  placement needed (very thin or very small mazes); earlier brainstorming
  of edge cases would have saved rework.

### Tools used

- `pytest` for unit tests (not submitted, used during development).
- `flake8` and `mypy --strict` for static analysis.
- `git` for version control, with feature branches per module reviewed by
  the other team member before merging.
