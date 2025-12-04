# Coordinates & Grid Operations

[← Back to README](../README.md)

The `aoc.coord` and `aoc.grid` modules provide utilities for working with 2D coordinate systems and grid-based puzzles.

## Table of Contents

- [Coord Class](#coord-class)
- [Direction Constants](#direction-constants)
- [Coordinate Operations](#coordinate-operations)
- [Grid Operations](#grid-operations)
- [Examples](#examples)

---

## Coord Class

Immutable coordinate class for 2D positions.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    row: int
    col: int
```

**Features:**
- **Immutable**: Safe to use as dictionary keys or in sets
- **Hashable**: Works in hash-based collections
- **Arithmetic**: Supports `+` and `-` operators
- **Type-safe**: Full type hints

### Creating Coordinates

```python
from aoc import Coord

# Direct construction
pos = Coord(row=0, col=0)
pos = Coord(5, 10)

# From tuples (using unpacking)
pos = Coord(*some_tuple)  # tuple must be (row, col)
```

### Arithmetic Operations

```python
# Addition (vector math)
new_pos = pos + Coord(1, 0)      # Move down
new_pos = pos + Coord.UP         # Move up (using direction constant)

# Subtraction (difference vector)
delta = pos2 - pos1
# If pos1=(1,1) and pos2=(3,4), delta=Coord(2,3)

# Chaining
final = start + Coord.RIGHT + Coord.DOWN
```

### Methods

#### `manhattan_distance(other: Coord) -> int`

Calculates Manhattan (taxicab) distance to another coordinate.

```python
pos1 = Coord(0, 0)
pos2 = Coord(3, 4)

distance = pos1.manhattan_distance(pos2)  # 7 (|3-0| + |4-0|)
```

#### `in_bounds(max_bounds: Coord, min_bounds: Coord = Coord(0, 0)) -> bool`

Checks if coordinate is within bounds.

```python
pos = Coord(5, 10)

# Check if within grid
is_valid = pos.in_bounds(Coord(20, 20))  # True (0 ≤ row < 20, 0 ≤ col < 20)

# Custom min bounds
is_valid = pos.in_bounds(Coord(20, 20), Coord(3, 5))  # True (3 ≤ row < 20, 5 ≤ col < 20)
```

#### `neighbors(max_bounds: Coord, directions: list[Coord] | None = None) -> list[Coord]`

Returns valid neighboring coordinates.

```python
pos = Coord(5, 5)
max_bounds = Coord(10, 10)

# Cardinal neighbors (default: UP, RIGHT, DOWN, LEFT)
neighbors = pos.neighbors(max_bounds)
# [Coord(4,5), Coord(5,6), Coord(6,5), Coord(5,4)]

# All 8 neighbors
neighbors = pos.neighbors(max_bounds, directions=Coord.DIRECTIONS_ALL)

# Custom directions (only right and down)
neighbors = pos.neighbors(max_bounds, directions=[Coord.RIGHT, Coord.DOWN])
```

---

## Direction Constants

Pre-defined direction vectors as class variables.

### Cardinal Directions

```python
Coord.ZERO = Coord(0, 0)

Coord.UP    = Coord(-1, 0)   # ↑
Coord.DOWN  = Coord(1, 0)    # ↓
Coord.LEFT  = Coord(0, -1)   # ←
Coord.RIGHT = Coord(0, 1)    # →
```

### Intercardinal (Diagonal) Directions

```python
Coord.UP_LEFT    = Coord(-1, -1)  # ↖
Coord.UP_RIGHT   = Coord(-1, 1)   # ↗
Coord.DOWN_LEFT  = Coord(1, -1)   # ↙
Coord.DOWN_RIGHT = Coord(1, 1)    # ↘
```

### Direction Collections

```python
# 4 cardinal directions [UP, RIGHT, DOWN, LEFT]
Coord.DIRECTIONS_CARDINAL

# 4 diagonal directions [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
Coord.DIRECTIONS_INTERCARDINAL

# All 8 directions (cardinals + diagonals)
Coord.DIRECTIONS_ALL
```

**Usage:**
```python
# Move in all cardinal directions
for direction in Coord.DIRECTIONS_CARDINAL:
    new_pos = current + direction
    # Process new_pos...

# Check all 8 neighbors
for direction in Coord.DIRECTIONS_ALL:
    neighbor = current + direction
    if neighbor.in_bounds(max_bounds):
        # Process neighbor...
```

### Rotation

Turn 90° clockwise or counter-clockwise:

```python
# Clockwise rotation
Coord.TURN_CLOCKWISE = {
    Coord.UP: Coord.RIGHT,
    Coord.RIGHT: Coord.DOWN,
    Coord.DOWN: Coord.LEFT,
    Coord.LEFT: Coord.UP,
}

# Counter-clockwise rotation
Coord.TURN_COUNTER_CLOCKWISE = {
    Coord.UP: Coord.LEFT,
    Coord.LEFT: Coord.DOWN,
    Coord.DOWN: Coord.RIGHT,
    Coord.RIGHT: Coord.UP,
}
```

**Usage:**
```python
facing = Coord.UP

# Turn right
facing = Coord.TURN_CLOCKWISE[facing]  # Now facing RIGHT

# Turn left
facing = Coord.TURN_COUNTER_CLOCKWISE[facing]  # Back to UP
```

---

## Coordinate Utilities

### `filter_coords_in_bounds(coords, max_bounds, min_bounds=Coord(0,0))`

Filters list of coordinates to only valid ones within bounds.

```python
from aoc import filter_coords_in_bounds, Coord

coords = [Coord(0,0), Coord(5,5), Coord(20,20), Coord(-1,0)]
max_bounds = Coord(10, 10)

valid = filter_coords_in_bounds(coords, max_bounds)
# [Coord(0,0), Coord(5,5)]  # Only these are within bounds
```

---

## Grid Operations

Functions for working with 2D lists (grids).

### Type Definition

```python
Grid = list[list[Any]]  # 2D grid type alias
```

### Grid Dimensions

#### `grid_size(grid) -> Coord`

Returns grid dimensions as Coord(rows, cols).

```python
from aoc import grid_size

grid = [['a', 'b'], ['c', 'd'], ['e', 'f']]

size = grid_size(grid)  # Coord(3, 2) - 3 rows, 2 columns
```

#### `grid_max_bounds(grid) -> Coord`

Returns maximum valid indices (size - 1).

```python
from aoc import grid_max_bounds

grid = [['a', 'b'], ['c', 'd'], ['e', 'f']]

max_bounds = grid_max_bounds(grid)  # Coord(2, 1) - max row=2, max col=1
```

**Use for bounds checking:**
```python
max_bounds = grid_max_bounds(grid)

for pos in positions:
    if pos.in_bounds(max_bounds):
        # Valid position
        value = grid_get(grid, pos)
```

### Bounds Checking

#### `grid_contains_coord(grid, coord) -> bool`

Checks if coordinate is valid for grid.

```python
from aoc import grid_contains_coord, Coord

grid = [[1, 2], [3, 4]]

grid_contains_coord(grid, Coord(0, 0))   # True
grid_contains_coord(grid, Coord(2, 0))   # False (out of bounds)
grid_contains_coord(grid, Coord(-1, 0))  # False (negative)
```

### Cell Access

#### `grid_get(grid, coord) -> Any`

Retrieves cell value at coordinate.

```python
from aoc import grid_get, Coord

grid = [['a', 'b'], ['c', 'd']]

value = grid_get(grid, Coord(0, 1))  # 'b'
value = grid_get(grid, Coord(1, 0))  # 'c'
```

#### `grid_set(grid, coord, value) -> None`

Sets cell value at coordinate.

```python
from aoc import grid_set, Coord

grid = [['a', 'b'], ['c', 'd']]

grid_set(grid, Coord(0, 1), 'X')
# grid is now [['a', 'X'], ['c', 'd']]
```

### Searching

#### `find_first(grid, value) -> Coord | None`

Finds first occurrence of value.

```python
from aoc import find_first

grid = [['#', '.', '#'], ['.', 'S', '.'], ['#', '.', '#']]

start = find_first(grid, 'S')  # Coord(1, 1)
wall = find_first(grid, '#')   # Coord(0, 0) - first '#' found
none = find_first(grid, 'X')   # None - not found
```

#### `find_all(grid, value) -> list[Coord]`

Finds all occurrences of value.

```python
from aoc import find_all

grid = [['#', '.', '#'], ['.', 'S', '.'], ['#', '.', '#']]

walls = find_all(grid, '#')  # [Coord(0,0), Coord(0,2), Coord(2,0), Coord(2,2)]
paths = find_all(grid, '.')  # [Coord(0,1), Coord(1,0), Coord(1,2), Coord(2,1)]
```

### Iteration

#### `grid_coords(grid) -> Iterator[tuple[Coord, Any]]`

Iterates over all cells with coordinates.

```python
from aoc import grid_coords

grid = [['a', 'b'], ['c', 'd']]

for position, value in grid_coords(grid):
    print(f"{position}: {value}")

# Output:
# Coord(0, 0): a
# Coord(0, 1): b
# Coord(1, 0): c
# Coord(1, 1): d
```

**Common pattern:**
```python
for position, value in grid_coords(grid):
    if value == '#':
        # Process walls
        pass
    elif value == '.':
        # Process paths
        pass
```

### Direction Search

#### `search_in_direction(grid, start, direction, target) -> bool`

Searches for string pattern in specific direction.

```python
from aoc import search_in_direction, Coord, read_data_as_char_grid

grid = read_data_as_char_grid("wordsearch")

start = Coord(0, 0)

# Search right for "XMAS"
found = search_in_direction(grid, start, Coord.RIGHT, "XMAS")

# Search all 8 directions
for direction in Coord.DIRECTIONS_ALL:
    if search_in_direction(grid, start, direction, "XMAS"):
        print(f"Found XMAS going {direction}")
```

### Grouping

#### `group_by_value(grid, exclude=None) -> dict[Any, list[Coord]]`

Groups coordinates by cell value.

```python
from aoc import group_by_value

grid = [['#', '.', '#'], ['.', '.', '#'], ['#', '.', '.']]

# Group all values
groups = group_by_value(grid)
# {
#     '#': [Coord(0,0), Coord(0,2), Coord(1,2), Coord(2,0)],
#     '.': [Coord(0,1), Coord(1,0), Coord(1,1), Coord(2,1), Coord(2,2)]
# }

# Exclude certain values
groups = group_by_value(grid, exclude='.')
# {'#': [Coord(0,0), Coord(0,2), Coord(1,2), Coord(2,0)]}

# Exclude multiple values
groups = group_by_value(grid, exclude={'.', '#'})
# {} - empty dict if all values excluded
```

**Use case - flood fill regions:**
```python
groups = group_by_value(grid, exclude='#')
for region_type, coords in groups.items():
    # Process each region
    pass
```

### Grid Creation

#### `create_visited_grid(size, initial_value=False) -> list[list[bool]]`

Creates boolean tracking grid.

```python
from aoc import create_visited_grid, Coord

size = Coord(10, 10)
visited = create_visited_grid(size)  # 10x10 grid of False

# Mark position as visited
visited[5][3] = True

# Check if visited
if visited[row][col]:
    # Already visited
    pass
```

#### `create_grid(size, initial_value=".") -> Grid`

Creates grid filled with initial value.

```python
from aoc import create_grid, Coord

size = Coord(5, 5)

# Create empty grid with '.'
grid = create_grid(size)
# [['.', '.', '.', '.', '.'],
#  ['.', '.', '.', '.', '.'],
#  ...]

# Create with custom value
grid = create_grid(size, initial_value='#')
# All cells are '#'
```

---

## Examples

### Example 1: Grid Navigation

```python
from aoc import (
    read_data_as_char_grid,
    Coord, grid_max_bounds, grid_get,
    find_first
)

def solve(data_file):
    grid = read_data_as_char_grid(data_file)
    max_bounds = grid_max_bounds(grid)
    start = find_first(grid, 'S')

    # Move in cardinal directions
    for direction in Coord.DIRECTIONS_CARDINAL:
        new_pos = start + direction
        if new_pos.in_bounds(max_bounds):
            value = grid_get(grid, new_pos)
            print(f"Neighbor: {value}")
```

### Example 2: Pathfinding Setup

```python
from aoc import (
    read_data_as_char_grid,
    find_first, grid_max_bounds,
    Coord
)

def setup_maze(data_file):
    grid = read_data_as_char_grid(data_file)
    start = find_first(grid, 'S')
    end = find_first(grid, 'E')
    max_bounds = grid_max_bounds(grid)

    return grid, start, end, max_bounds
```

### Example 3: Direction Search

```python
from aoc import (
    read_data_as_char_grid,
    grid_coords, search_in_direction,
    Coord
)

def count_word_occurrences(data_file, word):
    grid = read_data_as_char_grid(data_file)
    count = 0

    for position, value in grid_coords(grid):
        if value == word[0]:  # First letter match
            for direction in Coord.DIRECTIONS_ALL:
                if search_in_direction(grid, position, direction, word):
                    count += 1

    return count
```

### Example 4: Region Detection

```python
from aoc import read_data_as_char_grid, group_by_value

def analyze_regions(data_file):
    grid = read_data_as_char_grid(data_file)
    regions = group_by_value(grid, exclude='.')

    for region_type, positions in regions.items():
        print(f"Region '{region_type}': {len(positions)} cells")
        # Further processing...
```

### Example 5: Rotation Logic

```python
from aoc import Coord

def patrol(grid, start_pos, start_dir):
    pos = start_pos
    facing = start_dir

    while True:
        next_pos = pos + facing

        if not next_pos.in_bounds(grid_max_bounds(grid)):
            break  # Left the grid

        if grid_get(grid, next_pos) == '#':
            # Turn right on obstacle
            facing = Coord.TURN_CLOCKWISE[facing]
        else:
            # Move forward
            pos = next_pos
```

---

[← Back to README](../README.md) | [Next: Algorithms →](algorithms.md)
