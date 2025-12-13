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
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v3.0.0
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
- Supports Python 3.10, 3.11, 3.12, 3.13, and 3.14

## Quick Start

```python
# Flat imports (recommended)
from aoc import Input, Grid, Coord, bfs, dijkstra, TestCase, run

# Explicit 2D imports (optional)
from aoc.d2 import Coord, Grid, Dimension

# Explicit 3D imports (required for 3D)
from aoc.d3 import Coord, Grid, Dimension

# Module imports
from aoc.input import Input
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
input.as_float_grid()               # Grid of floating-point values
input.as_grid(str.upper)            # Grid with converter function
input.as_conditional_grid(lambda c: c if c.isdigit() else -1)  # Conditional conversion
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

**Pattern Extraction**
```python
extract_ints(text)                  # Extract all integers from text
extract_pattern(text, r"\d+")       # Extract regex matches
pattern_to_bools(".##.#")           # [False, True, True, False, True]
extract_bracketed("[data]")         # "data"
extract_parenthesized("(x,y)")      # ["x,y"]
extract_braced("{1,2,3}")           # "1,2,3"
```

**Raw Access**
```python
input.content                       # Raw string content
```

### Grid - 2D array with coordinate access

Wraps 2D arrays with coordinate-based indexing and search methods.

```python
grid = Grid([['#', '.', '#'],
             ['.', '.', '.'],
             ['#', '.', '#']])

# Access by coordinate
grid[Coord(1, 0)]                   # '.'  (x=1, y=0)
grid[coord] = 'X'                   # Set value
coord in grid                       # Check bounds

# Properties
grid.size                           # Dimension(width=3, height=3)
grid.max_bounds                     # Coord(x=2, y=2)

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
# Creation (using x, y)
coord = Coord(x=3, y=5)             # Mathematical x,y order
coord = Coord.from_rc(row=5, col=3) # From row,col format

# Access
coord.x, coord.y                    # Direct x, y access
coord.row, coord.col                # Grid-style access (y, x)

# Arithmetic
coord + Coord.RIGHT                 # Coord(x=4, y=5)
coord - other                       # Vector subtraction
coord.manhattan_distance(other)     # |Δx| + |Δy|
coord.euclidean_distance(other)     # √(Δx² + Δy²)
coord.squared_distance(other)       # Δx² + Δy² (faster)

# Bounds checking
coord.in_bounds(Coord(10, 10))      # Within (0,0) to (10,10)
coord.neighbors(max_bounds)         # Cardinal neighbors in bounds
coord.neighbors(max_bounds, Coord.DIRECTIONS_ALL)  # All 8 directions

# Direction constants
Coord.ZERO                          # Coord(0, 0)
Coord.UP, DOWN, LEFT, RIGHT         # Cardinal: y=-1, y=1, x=-1, x=1
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

### 3D Support - d3 module

Full 3D coordinate and grid system (requires explicit import).

```python
from aoc.d3 import Coord, Grid, Dimension

# 3D Coordinates
coord = Coord(x=1, y=2, z=3)
coord + Coord.FORWARD               # Move in z direction
coord.manhattan_distance(other)     # 3D Manhattan distance
coord.euclidean_distance(other)     # 3D Euclidean distance
coord.squared_distance(other)       # 3D squared distance

# 3D Directions
Coord.UP, DOWN, LEFT, RIGHT         # Standard 2D movement in 3D
Coord.FORWARD, BACK                 # Z-axis movement
Coord.DIRECTIONS_CARDINAL           # All 6 cardinal directions

# 3D Grid
grid = Grid.create(Dimension(10, 10, 10), '.')
grid[Coord(5, 5, 5)] = 'X'
coord in grid                       # 3D bounds checking
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

**Flood Fill - Region filling**
```python
# Non-destructive (returns coordinates)
region = flood_fill(grid, start, {'.', 'O'})     # Set of reachable coords

# Destructive (marks in-place)
flood_fill_mark(grid, start, 'X', {'.', 'O'})    # Marks region with 'X'
```

**Path Counting**
```python
# DAG path counting (memoized, efficient)
count = count_paths_dag(start, neighbors_func, goal_func)

# Cyclic graph path counting (backtracking)
count = count_paths_cyclic(start, neighbors_func, goal_func)
```

**Max Clique - Find largest fully-connected subgraph**
```python
graph = {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'}}
clique = find_max_clique(graph)                  # {'A', 'B', 'C'}
```

**UnionFind - Disjoint set union**
```python
uf = UnionFind()
uf.union('A', 'B')
uf.union('B', 'C')
uf.find('A') == uf.find('C')        # True (same component)
uf.get_component_sizes()            # {root: size, ...}
uf.count_components()               # Number of disjoint components
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

### Math - Number utilities

Common mathematical operations for puzzles.

```python
from aoc import count_continuous_segments, count_digits, calculate_toggle_states

# Count continuous segments
count_continuous_segments([1, 2, 2, 3, 3, 3, 4])  # 4 segments

# Count digits in number
count_digits(12345)                 # 5
count_digits(0)                     # 1

# Calculate final toggle states (parity-based)
toggles = {1: 3, 2: 2, 3: 1}        # Position: toggle count
states = calculate_toggle_states(toggles, 5)  # 5 positions
# Returns: {1: True, 2: False, 3: True, 4: False, 5: False}
```

### Testing - Test framework

Simple test framework with performance metrics.

```python
from aoc import TestCase, run

# Define test cases
test_cases = [
    TestCase(input_data="example1.txt", part1=42, part2=100),
    TestCase(input_data="example2.txt", part1=10),
]

# Run tests
def part1(input_data):
    return solve_part1(input_data)

def part2(input_data):
    return solve_part2(input_data)

run(test_cases, part1, part2)
# Displays: Pass/Fail, Expected/Got, Execution time, Memory usage
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

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and migration guides.

Current version: **3.0.0**
- 3D coordinate and grid support
- Enhanced graph algorithms (flood fill, path counting, union-find)
- Extended input parsing utilities
- Breaking: Coord now uses x,y instead of row,col attributes

## License

CC BY-NC-SA 4.0

## Links

- [Repository](https://github.com/jeffwindsor/aoc-toolkit)
- [Issues](https://github.com/jeffwindsor/aoc-toolkit/issues)
- [Changelog](CHANGELOG.md)
- [Migration Guide](MIGRATION.md)
