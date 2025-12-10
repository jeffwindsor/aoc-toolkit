# AOC Toolkit

Reusable utilities for Advent of Code puzzles.

## Installation

### From GitHub (Latest)

Install directly from the main branch:

```bash
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git
```

### From GitHub (Specific Version)

Install a specific release version:

```bash
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.4
```

### Development Installation

Clone and install in editable mode for development:

```bash
git clone https://github.com/jeffwindsor/aoc-toolkit.git
cd aoc-toolkit
pip install -e .
```

### Development with Testing Tools

Install with optional development dependencies:

```bash
pip install -e ".[dev]"
```

## Requirements

- Python 3.10 or higher
- Supports Python 3.10, 3.11, 3.12, and 3.14

## Quick Start

```python
# Flat imports (recommended)
from aoc import Input, Grid, Coord, bfs, dijkstra

# Explicit module imports
from aoc.input import Input
from aoc.grid import Grid
from aoc.coord import Coord
from aoc.graph import bfs, dijkstra
```

## API Reference

### Input - Parse AOC puzzle inputs

Flexible parser for common AOC input patterns. Create from file or string, then chain parsing methods.

```python
# From file
input = Input("data/puzzle.txt")

# From string
input = Input.from_string("1,2,3\n4,5,6")
```

**Lines & Sections**
```python
input.as_lines()                    # ["line1", "line2", "line3"]
input.as_sections()                 # Split on blank lines → [Input, Input, ...]
rules, updates = input.as_sections()  # Unpack two sections
```

**Grids**
```python
input.as_grid()                     # Grid of characters
input.as_int_grid()                 # Grid of digit ints (non-digits → -1)
input.as_grid(str.upper)            # Grid with converter function
```

**Coordinates**
```python
input.as_coords()                   # "6,1\n8,3" → [Coord(6,1), Coord(8,3)]
input.as_coords(separator=",")     # Custom separator
```

**Delimited Values**
```python
input.as_delimited_lines()          # "1,2,3\n4,5,6" → [[1,2,3], [4,5,6]]
input.as_delimited_lines(";", str)  # Custom separator and type
input.as_columns()                  # "1 2\n3 4" → [('1','3'), ('2','4')]
input.as_columns(converter=int)     # "1 2\n3 4" → [(1,3), (2,4)]
```

**Key-Value Pairs**
```python
input.as_key_value_pairs()          # "190: 10 19" → [(190, [10,19])]
input.as_key_value_pairs(str, str.split)  # Custom parsers
```

**Graph Edges**
```python
input.as_adjacency_list()           # "A-B\nB-C" → {'A':{'B'}, 'B':{'A','C'}, ...}
input.as_adjacency_list("-", directed=True)  # Directional edges
```

**Raw Access**
```python
input.content                       # Raw string content
extract_ints(text)                  # Extract all integers from text
extract_pattern(text, r"\d+")       # Extract regex matches
```

### Grid - 2D array with coordinate access

Wraps 2D arrays with coordinate-based indexing and search methods.

```python
grid = Grid([['#', '.', '#'],
             ['.', '.', '.'],
             ['#', '.', '#']])

# Access by coordinate
grid[Coord(0, 1)]                   # '.'
grid[coord] = 'X'                   # Set value
coord in grid                       # Check bounds

# Properties
grid.size                           # Dimension(width=3, height=3)
grid.max_bounds                     # Coord(col=2, row=2)

# Search
grid.find_first('.')                # First coord with value
grid.find_all('.')                  # All coords with value
grid.group_by_value(exclude='#')    # {'.': [coord1, coord2, ...]}

# Iteration
for coord, value in grid.coords():
    print(coord, value)

# Direction search
grid.search_in_direction(start, Coord.RIGHT, "XMAS")  # True if found

# Creation
Grid.create(Dimension(10, 10), '.')  # 10x10 grid filled with '.'
```

### Coord - 2D coordinates with direction support

Immutable coordinate class with vector operations and built-in directions.

```python
coord = Coord(row=5, col=3)
coord = Coord(5, 3)                 # Row-major order

# Arithmetic
coord + Coord.RIGHT                 # Coord(5, 4)
coord - other                       # Vector subtraction
coord.manhattan_distance(other)     # |Δrow| + |Δcol|

# Bounds checking
coord.in_bounds(Coord(10, 10))      # Within (0,0) to (10,10)
coord.neighbors(max_bounds)         # Cardinal neighbors in bounds
coord.neighbors(max_bounds, Coord.DIRECTIONS_ALL)  # All 8 directions

# Direction constants
Coord.ZERO                          # Coord(0, 0)
Coord.UP, DOWN, LEFT, RIGHT         # Cardinal: (-1,0), (1,0), (0,-1), (0,1)
Coord.UP_LEFT, UP_RIGHT             # Intercardinal diagonals
Coord.DOWN_LEFT, DOWN_RIGHT

# Direction sets
Coord.DIRECTIONS_CARDINAL           # [UP, RIGHT, DOWN, LEFT]
Coord.DIRECTIONS_INTERCARDINAL      # [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
Coord.DIRECTIONS_ALL                # All 8 directions

# Rotation
Coord.TURN_CLOCKWISE[direction]     # Rotate direction 90° CW
Coord.TURN_COUNTER_CLOCKWISE[dir]   # Rotate direction 90° CCW
```

**Dimension** - Grid size representation
```python
size = Dimension(width=10, height=5)  # 10 cols, 5 rows
```

### Graph - Search algorithms

Generic graph search algorithms that work with any hashable state.

**BFS - Breadth-first search**
```python
# Find all distances
distances = bfs(start, neighbors_func)           # {state: distance, ...}

# Find path to goal
path = bfs(start, neighbors_func, goal_func)     # [state1, state2, ...]

# Grid pathfinding (shortest path)
path = bfs_grid_path(grid, start, end, {'.', 'O'})  # walkable values
```

**DFS - Depth-first search**
```python
# Find any path to goal (not shortest)
path = dfs(start, neighbors_func, goal_func)     # [state1, state2, ...]

# Grid pathfinding
path = dfs_grid_path(grid, start, end, {'.', 'O'})
```

**Dijkstra - Weighted shortest path**
```python
def neighbors_func(coord):
    return [(neighbor, cost), ...]  # List of (state, cost) tuples

distances = dijkstra(start, neighbors_func)       # {state: min_cost, ...}
distances = dijkstra(start, neighbors_func, goal) # Early exit at goal
```

**Max Clique - Find largest fully-connected subgraph**
```python
graph = {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'}}
clique = find_max_clique(graph)                  # {'A', 'B', 'C'}
```

**Neighbor function pattern**
```python
# Simple neighbor function
def neighbors(coord):
    return [coord + d for d in Coord.DIRECTIONS_CARDINAL
            if (coord + d) in grid and grid[coord + d] != '#']

# Weighted neighbor function
def weighted_neighbors(coord):
    return [(coord + d, grid[coord + d])
            for d in Coord.DIRECTIONS_CARDINAL if (coord + d) in grid]

# State-based (for complex problems)
def state_neighbors(state):
    coord, direction = state
    return [((coord + direction, direction), 1),           # Move forward
            ((coord, turn_clockwise[direction]), 1000)]    # Turn
```

## Testing

Run tests locally:

```bash
# Install nox
pip install nox

# Run all tests across Python versions
nox

# Run tests for specific Python version
nox --python 3.14

# Run full validation (imports + tests)
nox -s validate_all
```

## License

CC BY-NC-SA 4.0

## Links

- [Repository](https://github.com/jeffwindsor/aoc-toolkit)
- [Issues](https://github.com/jeffwindsor/aoc-toolkit/issues)
