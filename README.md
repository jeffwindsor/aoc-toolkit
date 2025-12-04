# AOC Toolkit

A collection of reusable utilities for solving Advent of Code puzzles. Pure Python stdlib, zero external dependencies.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Tests](https://github.com/jeffwindsor/aoc-toolkit/workflows/Tests/badge.svg)

## Why This Toolkit?

- **Zero Dependencies** - Pure Python stdlib, works everywhere
- **41 Focused Utilities** - Every function solves a real AOC pattern
- **Type-Safe** - Full type hints for IDE support
- **Fast Setup** - Install directly from GitHub, no compilation
- **Battle-Tested** - Proven across multiple AOC years

## Quick Start

**Install:**
```bash
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0
```

**Use the [solution template](examples/template_solution.py):**
```python
from aoc import read_data_as_lines, run, TestCase, Coord, bfs

def solve(data_file):
    lines = read_data_as_lines(data_file)
    # Your solution here
    return result

if __name__ == "__main__":
    run(solve, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part1")
```

## Quick Reference

| Task | Function | Example |
|------|----------|---------|
| Read input | `read_data_as_lines` | `lines = read_data_as_lines("input")` |
| Parse grid | `read_data_as_char_grid` | `grid = read_data_as_char_grid("maze")` |
| Navigate | `Coord` + directions | `pos = Coord(0, 0) + Coord.UP` |
| Find in grid | `find_first`, `find_all` | `start = find_first(grid, 'S')` |
| Shortest path | `bfs`, `dijkstra` | `distances = bfs(start, neighbors)` |
| Test solutions | `run`, `TestCase` | `run(solve, [TestCase("example")])` |

## What's Included

**📁 Data I/O** - 10 functions for parsing inputs
- Read lines, grids, coordinates, graphs, sections
- Extract integers from text

**🧪 Testing** - Test runner with colored output
- Auto-load expected values from files
- Optional performance metrics

**🧭 Coordinates** - Immutable coordinate class
- Direction constants (UP, DOWN, LEFT, RIGHT, diagonals)
- Manhattan distance, bounds checking, neighbor finding

**🗺️ Grid Operations** - 12 functions for 2D grids
- Find values, iterate coordinates, search directions
- Group by value, create grids

**🕸️ Graph Algorithms** - Generic implementations
- BFS, DFS, Dijkstra, maximum clique
- Works with any hashable state type

**🔢 Math** - Common utilities
- Count continuous segments, count digits

**Total: 41 utilities | Zero dependencies | Python 3.10+**

## Import Styles

Choose the style that fits your use case:

```python
# Flat imports (quick scripts) - RECOMMENDED for AOC solutions
from aoc import read_data_as_lines, Coord, bfs, run, TestCase

# Module imports (shared code)
from aoc.data import read_data_as_lines
from aoc.coord import Coord
from aoc.graph import bfs

# Namespace imports (avoid conflicts)
import aoc.data
lines = aoc.data.read_data_as_lines("input")
```

All three styles remain stable across 1.x versions.

## Documentation

- [📁 Data I/O Guide](docs/data_io.md) - All parsing functions
- [🧪 Testing Guide](docs/testing.md) - Test framework details
- [🧭 Coordinates & Grids](docs/coordinates.md) - Coord class and grid operations
- [🕸️ Algorithms Guide](docs/algorithms.md) - Graph algorithms with examples
- [📦 Migration Guide](docs/migration.md) - Migrate existing projects

## Setup

### Installation

```bash
# Latest version
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git

# Specific version (recommended)
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0
```

### In requirements.txt
```
aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0
```

### In pyproject.toml
```toml
[project]
dependencies = [
    "aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0"
]
```

### Data File Structure

```
your_project/
├── solution.py
└── data/
    ├── example_01
    ├── example_01.part1.answer
    ├── puzzle_input
    └── puzzle_input.part1.answer
```

## Examples

### Grid Maze Solving

```python
from aoc import read_data_as_char_grid, find_first, dfs_grid_path, run, TestCase

def solve(data_file):
    grid = read_data_as_char_grid(data_file)
    start = find_first(grid, 'S')
    end = find_first(grid, 'E')

    path = dfs_grid_path(grid, start, end, walkable_values={'.', 'S', 'E'})
    return len(path) - 1 if path else -1

if __name__ == "__main__":
    run(solve, [TestCase("maze_example"), TestCase("maze_input")], part="part1")
```

### Graph Shortest Path

```python
from aoc import read_data_as_graph_edges, dijkstra, run, TestCase

def solve(data_file):
    graph = read_data_as_graph_edges(data_file)

    def neighbors(node):
        return [(neighbor, 1) for neighbor in graph[node]]

    distance = dijkstra('START', neighbors, goal='END')
    return distance if distance is not None else -1

if __name__ == "__main__":
    run(solve, [TestCase("graph_example")], part="part1")
```

### Grid Navigation

```python
from aoc import read_data_as_char_grid, Coord, grid_coords, run, TestCase

def solve(data_file):
    grid = read_data_as_char_grid(data_file)
    count = 0

    for position, value in grid_coords(grid):
        if value == 'X':
            for direction in Coord.DIRECTIONS_ALL:
                # Check for pattern in each direction
                count += check_pattern(grid, position, direction)

    return count

if __name__ == "__main__":
    run(solve, [TestCase("example")], part="part1")
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (2.0.0): Breaking changes
- **MINOR** (1.1.0): New features, backward-compatible
- **PATCH** (1.0.1): Bug fixes only

### Backward Compatibility Promise

Within 1.x versions:
- No breaking API changes
- Safe to upgrade from 1.0.0 → 1.9.9 without code changes
- Deprecations announced 2 MINOR releases in advance
- All import styles remain stable

**[View Releases & Changelog →](https://github.com/jeffwindsor/aoc-toolkit/releases)**

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing, and guidelines.

## License

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

You are free to:
- Use for personal projects
- Modify and adapt
- Share and distribute

Under these terms:
- **Attribution**: Credit the original
- **NonCommercial**: No commercial use without permission
- **ShareAlike**: Derivatives use same license

[Full License Text](LICENSE)

---

**Built for Advent of Code enthusiasts**
