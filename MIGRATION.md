# Migration Guide: 1.x → 2.0

This guide helps you migrate from aoc-toolkit 1.x to 2.0.

## Overview

Version 2.0 introduces **breaking changes** to the coordinate system and module organization, along with significant new features including 3D support and enhanced graph algorithms.

## Breaking Changes

### 1. Coordinate System Change

**What Changed**: `Coord` now uses `x, y` attributes instead of `row, col`.

#### Before (1.x):
```python
from aoc import Coord

c = Coord(row=5, col=10)
print(c.row, c.col)  # 5 10
```

#### After (2.0):
```python
from aoc import Coord

# Direct x, y construction
c = Coord(x=10, y=5)
print(c.x, c.y)      # 10 5
print(c.col, c.row)  # 10 5 (properties map x→col, y→row)

# Or use factory method for row, col
c = Coord.from_rc(row=5, col=10)
print(c.x, c.y)      # 10 5
print(c.row, c.col)  # 5 10
```

**Migration Strategy**:
1. **Quick fix**: Use `Coord.from_rc(row, col)` to maintain row/col semantics
2. **Preferred**: Switch to `Coord(x, y)` for mathematical consistency
3. **Properties work**: `coord.row` and `coord.col` still work as properties

### 2. Module Reorganization

**What Changed**: Coordinate and grid functionality combined into unified modules.

#### Before (1.x):
```python
from aoc.coord import Coord, Dimension
from aoc.grid import Grid
```

#### After (2.0):
```python
# Unified 2D module
from aoc.d2 import Coord, Grid, Dimension

# Or use convenience re-exports (recommended)
from aoc import Coord, Grid, Dimension
```

**Migration Strategy**:
1. **Simple projects**: Use `from aoc import Coord, Grid` (no changes needed if you were already using this)
2. **Explicit imports**: Update `from aoc.coord/grid import` → `from aoc.d2 import`
3. **Old imports deprecated**: `aoc.coord` and `aoc.grid` will be removed in 3.0

### 3. Direction Constants Location

**What Changed**: Direction constants moved to Coord class.

#### Before (1.x):
```python
from aoc.coord import Coord, DIRECTIONS_CARDINAL
```

#### After (2.0):
```python
from aoc import Coord

# Access via class
directions = Coord.DIRECTIONS_CARDINAL
up = Coord.UP
```

## New Features

### 3D Support

Version 2.0 adds full 3D coordinate and grid support:

```python
from aoc.d3 import Coord, Grid, Dimension

# 3D coordinates
pos = Coord(x=10, y=20, z=30)
print(pos.manhattan_distance(Coord(0, 0, 0)))  # 60

# 3D grids
grid_3d = Grid.create(Dimension(10, 10, 10), initial_value=0)
grid_3d[Coord(5, 5, 5)] = 42

# 6 cardinal directions
neighbors = pos.neighbors(max_bounds=Coord(100, 100, 100))
```

### Enhanced Graph Algorithms

New functions for common graph operations:

```python
from aoc import flood_fill, flood_fill_mark, count_paths_dag, UnionFind

# Flood fill (non-destructive)
visited = flood_fill(grid, start_coord, walkable_values={'.'})

# Flood fill with marking
count = flood_fill_mark(grid, start_coord, {'.'},  mark_value='X')

# Path counting
paths = count_paths_dag(start, target, neighbors_func)

# Union-Find for connectivity
uf = UnionFind(n=100)
uf.union(0, 1)
uf.union(1, 2)
print(uf.count_components())
```

### New Input Utilities

```python
from aoc import pattern_to_bools, extract_bracketed

# Pattern to booleans
bools = pattern_to_bools(".##.#")  # [False, True, True, False, True]

# Extract from brackets
content = extract_bracketed("[data]")  # "data"
```

### New Math Utilities

```python
from aoc import calculate_toggle_states

# Calculate toggle states (parity-based)
states = calculate_toggle_states([0, 1, 0, 2], size=3)
# [False, True, True] - element toggled odd times = True
```

## Step-by-Step Migration

### Step 1: Update Package Version

```bash
pip install --upgrade aoc-toolkit
# Or with editable install
pip install -e path/to/aoc-toolkit
```

### Step 2: Update Imports

**Find and replace** in your codebase:

```python
# Old imports → New imports
from aoc.coord import → from aoc.d2 import
from aoc.grid import → from aoc.d2 import

# Or simplify to:
from aoc import Coord, Grid, Dimension
```

### Step 3: Update Coord Construction

**Option A: Use from_rc factory** (minimal changes):
```python
# Before: Coord(5, 10)
# After:   Coord.from_rc(5, 10)
```

**Option B: Switch to x/y** (preferred):
```python
# Before: Coord(row=5, col=10)
# After:   Coord(x=10, y=5)  # Note: x=col, y=row
```

### Step 4: Test Your Code

Run your test suite to catch any issues:

```bash
pytest
# or
python -m pytest
```

### Step 5: Adopt New Features (Optional)

Take advantage of new functionality:
- Add 3D support where needed
- Use flood_fill for grid exploration
- Use UnionFind for connectivity problems
- Try new input/math utilities

## Common Migration Issues

### Issue 1: Coordinate Index Confusion

**Problem**: Getting `x` and `y` confused with `row` and `col`.

**Solution**: Remember the mapping:
- `x` = column (horizontal position)
- `y` = row (vertical position)
- `coord.row` property = `coord.y`
- `coord.col` property = `coord.x`

### Issue 2: Grid Indexing

**Problem**: Grid[coord] not working as expected after coordinate change.

**Solution**: Grid indexing uses `coord.row` and `coord.col` internally, so it should work transparently. If you were manually indexing with `grid.data[row][col]`, update to use `grid[coord]` instead.

### Issue 3: Import Errors

**Problem**: `ImportError: cannot import name 'Coord' from 'aoc.coord'`

**Solution**: Update imports to use `aoc.d2` or the top-level `aoc` package.

## Deprecation Timeline

- **Version 2.0**: `aoc.coord` and `aoc.grid` imports still work but are deprecated
- **Version 2.1**: Deprecation warnings added
- **Version 3.0**: Old imports will be removed

## Need Help?

- Check the [CHANGELOG.md](CHANGELOG.md) for all changes
- See [README.md](README.md) for updated documentation
- Review the [examples](examples/) directory for usage patterns
- Open an issue on GitHub if you encounter problems

## Quick Reference

### Import Cheat Sheet

| 1.x | 2.0 (Recommended) | 2.0 (Explicit) |
|-----|-------------------|----------------|
| `from aoc.coord import Coord` | `from aoc import Coord` | `from aoc.d2 import Coord` |
| `from aoc.grid import Grid` | `from aoc import Grid` | `from aoc.d2 import Grid` |
| `from aoc.coord import Dimension` | `from aoc import Dimension` | `from aoc.d2 import Dimension` |

### Coord Constructor Cheat Sheet

| Pattern | 1.x | 2.0 |
|---------|-----|-----|
| **Row/Col** | `Coord(5, 10)` | `Coord.from_rc(5, 10)` |
| **X/Y** | N/A | `Coord(10, 5)` |
| **Named** | `Coord(row=5, col=10)` | `Coord(x=10, y=5)` |

### Property Mapping

| 2.0 Property | Maps To |
|--------------|---------|
| `coord.x` | Column position |
| `coord.y` | Row position |
| `coord.col` | `coord.x` |
| `coord.row` | `coord.y` |
