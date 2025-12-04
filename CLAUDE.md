# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**aoc-toolkit** is a Python library providing reusable utilities for Advent of Code puzzles. It's designed as a zero-dependency, pure Python stdlib package distributed via direct GitHub installation (not PyPI).

**Key Constraints:**
- **Zero external dependencies** - Pure Python stdlib only
- **Python 3.10+** minimum version
- **CC BY-NC-SA 4.0** license - Non-commercial use only
- **Semantic versioning** with backward compatibility promise within 1.x.x releases

## Architecture

### Package Structure

```
src/aoc/
├── __init__.py          # Package entry point, exports flat API
├── coord.py             # Immutable Coord class with direction constants
├── grid.py              # 2D grid operations (12 functions)
├── graph.py             # Graph algorithms (BFS, DFS, Dijkstra, max clique)
├── data.py              # I/O utilities (10 parsing functions)
├── math.py              # Mathematical utilities
└── testing.py           # Test framework with performance metrics
```

### Import Philosophy

The package supports **three import styles** for maximum flexibility:

1. **Flat imports** (recommended for AOC scripts): `from aoc import Coord, bfs, run`
2. **Explicit module imports** (recommended for libraries): `from aoc.coord import Coord`
3. **Namespace imports** (most explicit): `import aoc.coord; aoc.coord.Coord(0, 0)`

**Critical:** All exports in `__init__.py` must be kept in sync with individual modules. The `__all__` list is the canonical source of public API.

### Core Design Patterns

**Coord as Foundation:**
- Immutable dataclass with frozen=True
- Direction constants defined as ClassVar (UP, DOWN, LEFT, RIGHT, etc.)
- Used as primary type for all grid and coordinate operations
- Supports arithmetic operations (+, -)

**Grid Representation:**
- Type alias: `Grid = list[list[Any]]`
- Row-major ordering: `grid[row][col]`
- Functions use `Coord` for position arguments, not (x, y) tuples
- Bounds checking uses inclusive max_bounds: `Coord(max_row, max_col)`

**Graph Algorithms:**
- Generic implementations work with any hashable state type
- Neighbor functions: `Callable[[State], list[State]]` or `Callable[[State], list[tuple[State, cost]]]`
- Goal functions: `Callable[[State], bool]`
- Grid-specific variants (e.g., `dfs_grid_path`) use walkable value sets

**Data I/O Convention:**
- All functions expect files in `./data/` directory
- Answer files: `data/{name}.{part}.answer` (e.g., `example_01.part1.answer`)
- Functions throw descriptive FileNotFoundError and IOError

**Testing Framework:**
- Performance tracking controlled by `.aoc_config` file: `test_performance_tracking=true`
- TestCase loads expected from answer files if no explicit value provided
- Colored output: TITLE_COLOR (blue), TRUE_COLOR (green), FALSE_COLOR (red)

## Development Commands

### Installation for Development

```bash
# Install in editable mode for local development
pip install -e .

# Install from GitHub (as users would)
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0
```

### Version Management

**Version is in TWO places** (must be kept in sync):
1. `pyproject.toml` - `version = "1.0.0"`
2. `README.md` - Changelog section at bottom

### Testing

We use **pytest** with **nox** for professional cross-platform testing.

**Install dev dependencies:**
```bash
pip install -e ".[dev]"
```

**Quick testing (fast iteration):**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_coord.py

# Run specific test
pytest tests/test_coord.py::TestCoord::test_addition -v
```

**Full validation (before committing):**

```bash
# Validate imports + run tests
nox -s validate_all

# Test all Python versions (3.10, 3.11, 3.12)
nox

# Generate coverage report
nox -s coverage

# Validate import styles only
nox -s validate_imports
```

**Test Coverage:**
- `test_coord.py` - Coord class, directions, rotations, bounds checking
- `test_grid.py` - Grid operations, find functions, iteration
- `test_graph.py` - BFS, DFS, Dijkstra, max clique algorithms
- `test_math.py` - Math utility functions

**CI/CD:**
- Tests run automatically via nox on all pushes and PRs (`.github/workflows/test.yml`)
- Tests run on Python 3.10, 3.11, 3.12 across Ubuntu, macOS, Windows
- Import validation included in CI pipeline
- Releases only created after all tests pass

### Release Process

**Automated via release script:**

```bash
# Simple usage (prompts for changelog)
./scripts/release.sh 1.0.1

# With changelog message
./scripts/release.sh 1.0.1 -m "Fix grid bounds checking"

# Dry run (preview changes without executing)
./scripts/release.sh 1.0.1 -m "Add new feature" --dry-run
```

**What the script does:**
1. Validates version format (MAJOR.MINOR.PATCH)
2. Checks version is greater than latest git tag
3. Verifies git working directory is clean
4. Prompts for changelog message (if not provided with -m)
5. Updates all 3 version locations atomically:
   - `pyproject.toml`
   - `src/aoc/__init__.py`
   - `README.md` (adds changelog entry)
6. Creates commit: `Release v1.X.Y: [description]`
7. Creates and pushes tag `v1.X.Y`

**GitHub Actions then automatically:**
- Runs all tests on Python 3.10, 3.11, 3.12
- Creates GitHub release if tests pass
- Extracts changelog from README.md
- Adds installation instructions

**Manual process (without script):**

```bash
# 1. Update version in all three locations manually
# 2. Commit changes
git add -A && git commit -m "Release v1.X.Y: [description]"

# 3. Create and push tag
git tag -a v1.X.Y -m "Release v1.X.Y"
git push origin v1.X.Y
```

### Documentation

Documentation lives in `docs/`:
- `algorithms.md` - Graph algorithms guide
- `coordinates.md` - Coord class and grid operations
- `data_io.md` - All data reading functions
- `migration.md` - Migration guide for existing projects
- `testing.md` - Test framework usage

## Code Guidelines

### Type Hints
- **Required** for all public functions
- Use `from typing import` for complex types
- Grid type: `list[list[Any]]` or specific: `list[list[str]]`, `list[list[int]]`
- Use `ClassVar` for class-level constants in dataclasses

### Docstrings
- **Required** for all public functions
- Google-style format with Args, Returns, and Examples sections
- Include input/output examples for data parsing functions

### Error Handling
- Raise descriptive errors with context (file paths, expected format)
- Data functions: FileNotFoundError and IOError with filenames
- Graph functions: ValueError for invalid inputs

### Backward Compatibility
Within 1.x.x versions:
- **Never** break existing API signatures
- **Never** change public function names
- **Never** remove exports from `__all__`
- Deprecations require 2 MINOR releases advance notice
- All three import styles must remain stable

### Testing Philosophy
The library has a comprehensive test suite covering core functionality (coord, grid, graph, math modules). Tests ensure backward compatibility and prevent regressions.

**When adding new features:**
1. Add tests to appropriate `tests/test_*.py` file
2. Test all public API functions
3. Include edge cases (empty inputs, boundary conditions)
4. Verify tests pass locally before committing

## Common Patterns

### Adding New Data Parser
1. Add function to `data.py` with full docstring and type hints
2. Export from `data.py` (if using `__all__`)
3. Add to `__init__.py` imports and `__all__` list
4. Add tests to `tests/test_data.py` (if practical without fixture files)
5. Document in `docs/data_io.md`

### Adding New Grid Operation
1. Add to `grid.py` - use `Coord` for positions
2. Type hint Grid parameter as `list[list[Any]]` or specific type
3. Export in `__init__.py`
4. Add tests to `tests/test_grid.py`
5. Document in `docs/coordinates.md`

### Adding New Direction to Coord
1. Define as ClassVar in Coord class
2. Update DIRECTIONS_* collections if appropriate
3. Document in `docs/coordinates.md`

## Performance Considerations

- Data functions cache nothing - always read from disk
- Coord is immutable - safe for dict keys and set membership
- Grid operations are not optimized for massive grids (AOC rarely exceeds 1000x1000)
- Graph algorithms use standard Python containers (dict, set, list)
