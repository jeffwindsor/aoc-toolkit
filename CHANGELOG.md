# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-12-13

### ⚠️ BREAKING CHANGES

- **Coordinate System**: `Coord` now uses `x, y` attributes instead of `row, col`
  - `row` and `col` are now properties mapping to `y` and `x` respectively
  - Added `Coord.from_rc(row, col)` factory method for row/col creation
  - This change makes coordinates more mathematical and consistent with standard conventions

- **Module Reorganization**: Combined coordinate and grid functionality
  - `aoc.coord` + `aoc.grid` → `aoc.d2` (unified 2D module)
  - Old imports (`from aoc.coord import Coord`) still work but are deprecated
  - Recommended: `from aoc.d2 import Coord, Grid, Dimension`

### ✨ Added

#### 3D Support (Major Feature)
- **New `d3` module** for 3D coordinate and grid operations
  - `Coord(x, y, z)` for 3D coordinates
  - `Dimension(width, height, depth)` for 3D dimensions
  - `Grid` for 3D array operations
  - 6 cardinal directions (UP, DOWN, LEFT, RIGHT, FORWARD, BACK)
  - Distance metrics: Manhattan, Euclidean, squared distance
  - Requires explicit import: `from aoc.d3 import Coord, Grid`

#### Graph Algorithms
- `flood_fill()` - Non-destructive flood fill returning reachable coordinates
- `flood_fill_mark()` - Destructive flood fill marking cells in-place
- `count_paths_dag()` - Count all paths in directed acyclic graphs (memoized)
- `count_paths_cyclic()` - Count all paths in cyclic graphs (backtracking)
- `UnionFind` class - Disjoint set union for connectivity problems
  - `find(x)` - Find root with path compression
  - `union(x, y)` - Union by rank
  - `get_component_sizes()` - Get sizes of all components
  - `count_components()` - Count number of components

#### Input Utilities
- `pattern_to_bools()` - Convert character patterns to boolean lists
- `extract_bracketed()` - Extract content from square brackets `[...]`
- `extract_parenthesized()` - Extract content from parentheses `(...)`
- `extract_braced()` - Extract content from curly braces `{...}`
- `as_conditional_grid()` - Parse grids with conditional value conversion
- `as_float_grid()` - Parse grids of floating-point values
- Enhanced string stripping control for flexible whitespace handling

#### Math Utilities
- `calculate_toggle_states()` - Calculate final states after multiple toggles (parity-based)
- `count_continuous_segments()` - Count continuous segments in sequences
- `count_digits()` - Count digits in numbers

#### Coordinate Enhancements
- `Coord.from_rc(row, col)` - Create coordinate from row/col format
- `squared_distance()` - Squared Euclidean distance (faster than Euclidean)
- `euclidean_distance()` - Euclidean distance calculation
- `.row` and `.col` properties for grid-style access

### 🔧 Changed

- Module structure reorganized for better coherence
- Default imports now come from `d2` module
- Improved consistency in coordinate system across 2D and 3D
- Enhanced test coverage for input parsing methods

### 📝 Documentation

- Added CHANGELOG.md for version tracking
- Added MIGRATION.md for upgrade guidance from 1.x to 2.0+
- Documentation improvements and clarifications

### 🧪 Testing

- All new features tested and validated
- Backward compatibility verified for major operations
- 3D module fully functional and tested

## [2.0.1] - 2025-12-09

### 📝 Documentation

- Added comprehensive API documentation to README
- Initial new README with usage examples
- Improved code examples and usage patterns

## [2.0.0] - 2025-12-09

### ⚠️ BREAKING CHANGES

- **Complete API Redesign**: Major refactoring for cleaner, more intuitive interface
  - Replaced `data.py` parsing approach with unified `Input` class
  - Simplified testing framework
  - Streamlined module organization

### ✨ Added

- **New `Input` class**: Unified, chainable interface for parsing AOC inputs
  - `as_lines()` - Split into lines
  - `as_grid()` - Parse character grids
  - `as_int_grid()` - Parse integer grids
  - `as_coords()` - Parse coordinate lists
  - `as_delimited_lines()` - Parse CSV-style data
  - `as_columns()` - Transpose columns
  - `as_adjacency_list()` - Parse graph edges
  - `as_key_value_pairs()` - Parse key-value formats
  - `as_sections()` - Split on blank lines
- `extract_ints()` - Extract all integers from text
- `extract_pattern()` - Extract regex pattern matches

### 🔧 Changed

- Completely rewrote input parsing system for flexibility
- Simplified testing framework
- Refactored coordinate, grid, and graph modules for consistency
- Improved type hints and documentation

### 🗑️ Removed

- Old `data.py` module and `Parser` class (replaced by `Input`)
- Extensive documentation files (replaced with concise README)
- Example templates (users should use their own patterns)

## [1.0.1] - 2025-12-05

### 🔧 Fixed

- CI/CD pipeline fixes
- Minor build and deployment improvements

## [1.0.0] - 2025-12-04

### ✨ Initial Release

- Basic 2D coordinate and grid operations
  - `Coord` class with cardinal and intercardinal directions
  - `Grid` class for 2D array operations
  - Direction constants and rotation helpers
- Core graph algorithms
  - BFS (breadth-first search)
  - DFS (depth-first search)
  - Dijkstra's algorithm for weighted shortest paths
  - `find_max_clique()` for maximum clique detection
  - Grid pathfinding helpers (`bfs_grid_path`, `dfs_grid_path`)
- Input parsing utilities via `data.py` and `Parser` class
- Math utilities
  - `count_continuous_segments()`
- Testing framework
  - `TestCase` class for puzzle test cases
  - `run()` function for test execution with performance metrics

---

## Migration Guides

### Upgrading from 2.x to 3.0

**Coordinate System Change:**
```python
# Old (2.x)
coord = Coord(row=5, col=3)
value = coord.row, coord.col

# New (3.0)
coord = Coord.from_rc(row=5, col=3)  # or Coord(x=3, y=5)
value = coord.row, coord.col  # Still works via properties
```

**Module Imports:**
```python
# Old (2.x)
from aoc.coord import Coord
from aoc.grid import Grid

# New (3.0 - recommended)
from aoc.d2 import Coord, Grid

# Or still use flat imports
from aoc import Coord, Grid
```

For 3D operations:
```python
from aoc.d3 import Coord, Grid, Dimension
```

### Upgrading from 1.x to 2.0

**Input Parsing:**
```python
# Old (1.x)
from aoc.data import Parser
data = Parser.from_file("input.txt").as_lines()

# New (2.0+)
from aoc import Input
data = Input("input.txt").as_lines()
```

See [MIGRATION.md](MIGRATION.md) for complete upgrade instructions.
