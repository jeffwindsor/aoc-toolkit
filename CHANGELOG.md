# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-13

### ⚠️ BREAKING CHANGES

- **Coordinate System**: `Coord` now uses `x, y` attributes instead of `row, col`
  - `row` and `col` are now properties mapping to `y` and `x` respectively
  - Added `Coord.from_rc(row, col)` factory method for row/col creation
  - This change makes coordinates more mathematical and consistent with standard conventions

- **Module Reorganization**: Combined coordinate and grid functionality
  - `aoc.coord` + `aoc.grid` → `aoc.d2` (unified 2D module)
  - Old imports still work temporarily but are deprecated
  - Update imports: `from aoc.d2 import Coord, Grid, Dimension`

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
- `extract_bracketed()` - Extract content from square brackets
- `extract_parenthesized()` - Extract content from parentheses (all occurrences)
- `extract_braced()` - Extract content from curly braces

#### Math Utilities
- `calculate_toggle_states()` - Calculate final states after multiple toggles (parity-based)

#### Coordinate Enhancements
- `Coord.from_rc(row, col)` - Create coordinate from row/col format
- `Coord.squared_distance()` - Squared Euclidean distance (faster than Euclidean)
- `Coord.euclidean_distance()` - Euclidean distance calculation
- `.row` and `.col` properties for grid-style access

### 🔧 Changed

- Module structure reorganized for better coherence
- Default imports now come from `d2` module
- Improved consistency in coordinate system across 2D and 3D

### 📝 Documentation

- Added CHANGELOG.md for version tracking
- Added MIGRATION.md for upgrade guidance
- Updated README.md with new features and import patterns
- Added in-situ-development.md for development workflow

### 🧪 Testing

- All new features tested and validated
- Backward compatibility verified for major operations
- 3D module fully functional and tested

## [1.0.4] - 2024-12-09

### Initial Release
- Basic 2D coordinate and grid operations
- Core graph algorithms (BFS, DFS, Dijkstra, max clique)
- Input parsing utilities
- Math utilities
- Test framework

---

## Migration Guide

See [MIGRATION.md](MIGRATION.md) for detailed upgrade instructions from 1.x to 2.0.

## Future Plans

- Expand 3D support based on usage patterns
- Add more graph algorithms as needed
- Enhance input parsing for common AoC patterns
- Comprehensive test suite for all modules
