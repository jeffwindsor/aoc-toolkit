# Contributing to aoc-toolkit

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to aoc-toolkit.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Guidelines](#code-guidelines)
- [Release Process](#release-process)
- [Getting Help](#getting-help)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of Advent of Code problem-solving patterns

### Setup Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/aoc-toolkit.git
   cd aoc-toolkit
   ```

2. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/jeffwindsor/aoc-toolkit.git
   ```

3. **Install in editable mode with dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   python -c "from aoc import Coord, bfs; print('✓ Installation successful')"
   ```

## Development Workflow

### 1. Create a Feature Branch

Always work on a feature branch, never directly on `main`:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `test/description` - Test additions/fixes

### 2. Make Your Changes

Follow our [code guidelines](#code-guidelines) when making changes.

### 3. Add Tests

**All new functionality requires tests.** Add tests in the appropriate `tests/test_*.py` file:

- `tests/test_coord.py` - Coord class tests
- `tests/test_grid.py` - Grid operation tests
- `tests/test_graph.py` - Graph algorithm tests
- `tests/test_math.py` - Math utility tests
- `tests/test_data.py` - Data I/O tests (if adding new parsers)

Example test:

```python
def test_new_feature(self):
    """Test the new feature works correctly."""
    result = my_new_function(input_data)
    self.assertEqual(result, expected_output)

    # Test edge cases
    self.assertEqual(my_new_function([]), expected_for_empty)
```

### 4. Run Tests Locally

We use **pytest** and **nox** for professional testing workflow:

**Quick iteration during development:**
```bash
# Run all tests with pytest (fast)
pytest

# Run specific test file
pytest tests/test_coord.py

# Run specific test
pytest tests/test_coord.py::TestCoord::test_addition -v

# Run with coverage
pytest --cov
```

**Full validation before committing:**
```bash
# Run tests on current Python version
nox -s tests

# Run tests on all Python versions (3.10, 3.11, 3.12)
nox

# Run with coverage report
nox -s coverage

# Validate all import styles
nox -s validate_imports

# Full validation (imports + tests)
nox -s validate_all
```

**Before committing**, ensure tests pass:
```bash
nox -s validate_all
```

### 5. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add -A
git commit -m "Add feature: description of what you added"
```

Good commit messages:
- `Add grid_contains_all function for multi-value search`
- `Fix off-by-one error in grid bounds checking`
- `Update documentation for Coord.neighbors method`

Bad commit messages:
- `fix bug`
- `update`
- `changes`

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub. In your PR description:
- Explain what changes you made and why
- Reference any related issues (e.g., "Fixes #123")
- Describe how you tested the changes

### 7. Code Review Process

- GitHub Actions will automatically run tests on multiple Python versions
- A maintainer will review your code
- Address any feedback by pushing new commits to your branch
- Once approved, a maintainer will merge your PR

## Testing

### Test Framework

We use **pytest** with **nox** for cross-platform, multi-version testing:

- **pytest**: Modern test framework with better output and fixtures
- **pytest-cov**: Coverage reporting with HTML reports
- **nox**: Automated testing across Python 3.10, 3.11, 3.12

### Test Structure

Tests use Python's `unittest.TestCase` (pytest-compatible):

```python
import unittest
from aoc import Coord

class TestCoord(unittest.TestCase):
    def test_addition(self):
        """Test coordinate addition."""
        c1 = Coord(1, 2)
        c2 = Coord(3, 4)
        result = c1 + c2
        self.assertEqual(result, Coord(4, 6))
```

### Running Tests

**Development (fast iteration):**
```bash
pytest                                    # All tests
pytest tests/test_coord.py               # Specific file
pytest tests/test_coord.py::TestCoord::test_addition  # Specific test
pytest -v                                 # Verbose output
pytest --cov                              # With coverage
```

**Pre-commit validation:**
```bash
nox -s validate_all                       # Import validation + tests
nox                                       # Test all Python versions
nox -s coverage                           # Generate coverage report
```

### Test Requirements

- **Test all public API functions** - Every function exported in `__all__` needs tests
- **Test edge cases** - Empty inputs, boundary conditions, invalid inputs
- **Test return types** - Verify functions return expected types
- **Use descriptive test names** - `test_grid_get_returns_none_for_out_of_bounds`
- **Include docstrings** - Explain what the test validates

### Import Validation

Nox automatically validates all three import styles:

```python
# Flat imports (for scripts)
from aoc import Coord, bfs, run

# Explicit module imports (for libraries)
from aoc.coord import Coord
from aoc.graph import bfs

# Namespace imports (most explicit)
import aoc.coord
aoc.coord.Coord(0, 0)
```

Run validation: `nox -s validate_imports`

### Coverage Reports

Generate coverage reports:
```bash
nox -s coverage
```

View HTML report: `open htmlcov/index.html`

### CI Testing

GitHub Actions automatically tests PRs using nox:
- Python 3.10, 3.11, 3.12
- Ubuntu, macOS, Windows
- Import validation + full test suite

Your PR must pass all CI tests before merging.

## Code Guidelines

### Python Style

- **Zero external dependencies** - Pure Python stdlib only
- **Python 3.10+** - Use modern Python features (match/case, union types, etc.)
- **Type hints required** - All public functions must have type hints
- **Docstrings required** - Google-style with examples

Example function:

```python
def grid_get(grid: Grid, coord: Coord) -> Any:
    """
    Get value at coordinate in grid.

    Args:
        grid: 2D grid (list of lists)
        coord: Coordinate position

    Returns:
        Value at the specified coordinate

    Examples:
        >>> grid = [['A', 'B'], ['C', 'D']]
        >>> grid_get(grid, Coord(0, 1))
        'B'
    """
    return grid[coord.row][coord.col]
```

### Design Principles

1. **Generic implementations** - Work with any hashable type where possible:
   ```python
   # Good - works with any state type
   def bfs(start: Any, neighbors_func: Callable[[Any], list[Any]]) -> dict[Any, int]:

   # Bad - hardcoded to Coord
   def bfs(start: Coord, neighbors_func: Callable[[Coord], list[Coord]]) -> dict[Coord, int]:
   ```

2. **Immutable data structures** - Use frozen dataclasses:
   ```python
   @dataclass(frozen=True)
   class Coord:
       row: int
       col: int
   ```

3. **Simple over complex** - Prefer straightforward implementations:
   ```python
   # Good - clear and simple
   def find_first(grid: Grid, value: Any) -> Coord | None:
       for r, row in enumerate(grid):
           for c, cell in enumerate(row):
               if cell == value:
                   return Coord(r, c)
       return None

   # Bad - unnecessarily complex
   def find_first(grid: Grid, value: Any) -> Coord | None:
       return next((Coord(r, c) for r, row in enumerate(grid)
                   for c, cell in enumerate(row) if cell == value), None)
   ```

4. **Consistent conventions** - Follow existing patterns:
   - Grid functions use `Coord` for positions
   - Coordinate system uses row-major ordering: `grid[row][col]`
   - Bounds are inclusive: `Coord(max_row, max_col)`
   - Direction constants are ClassVar on Coord

### Backward Compatibility

Within 1.x.x versions, we promise:
- No breaking changes to existing APIs
- All three import styles remain stable
- Safe to upgrade 1.0.0 → 1.9.9 without code changes
- Deprecations announced 2 MINOR releases in advance

**When adding features:**
- Add new functions (good)
- Add optional parameters with defaults (good)
- Change function signatures (bad)
- Remove functions (bad)
- Change return types (bad)

### Adding New Functions

When adding a new function, update all relevant locations:

1. **Add function to module** (e.g., `src/aoc/grid.py`)
2. **Add to module's `__all__`** (if it has one)
3. **Add to `src/aoc/__init__.py`**:
   - Import in imports section
   - Add to `__all__` list
4. **Add tests** to `tests/test_*.py`
5. **Update documentation** in `docs/*.md`

## Release Process

**For maintainers only.** Contributors don't need to worry about releases.

### Using the Release Script

The release script automates the entire version bump process:

```bash
# Interactive mode (prompts for changelog)
./scripts/release.sh 1.0.1

# With changelog message
./scripts/release.sh 1.0.1 -m "Fix grid bounds checking"

# Preview changes without executing
./scripts/release.sh 1.0.1 -m "Add new feature" --dry-run
```

### What the Script Does

1. **Validates version**:
   - Checks format is `MAJOR.MINOR.PATCH`
   - Ensures new version is greater than latest git tag
   - Verifies working directory is clean

2. **Updates version** in three locations:
   - `pyproject.toml`
   - `src/aoc/__init__.py`
   - `README.md` (adds dated changelog entry)

3. **Creates release**:
   - Commits changes with message: `Release v1.X.Y: [description]`
   - Creates git tag: `v1.X.Y`
   - Pushes tag to trigger GitHub Actions

4. **Automated release** (GitHub Actions):
   - Runs tests on Python 3.10, 3.11, 3.12
   - Creates GitHub Release if tests pass
   - Extracts changelog from README.md
   - Notifies with installation instructions

### Version Bumping Guide

Follow semantic versioning:

- **PATCH** (1.0.X) - Bug fixes, no API changes
  ```bash
  ./scripts/release.sh 1.0.1 -m "Fix off-by-one error in grid bounds"
  ```

- **MINOR** (1.X.0) - New features, backward-compatible
  ```bash
  ./scripts/release.sh 1.1.0 -m "Add grid_contains_all function"
  ```

- **MAJOR** (X.0.0) - Breaking changes (avoid within 1.x.x)
  ```bash
  ./scripts/release.sh 2.0.0 -m "Redesigned grid API for consistency"
  ```

### Manual Release (Without Script)

If the script is unavailable:

1. Update version in `pyproject.toml`, `src/aoc/__init__.py`, `README.md`
2. Commit: `git commit -m "Release v1.X.Y: description"`
3. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
4. Push: `git push origin v1.X.Y`

## Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/jeffwindsor/aoc-toolkit/discussions)
- **Bug reports?** Open a [GitHub Issue](https://github.com/jeffwindsor/aoc-toolkit/issues)
- **Documentation unclear?** PRs to improve docs are welcome!

## Thank You!

Your contributions help make Advent of Code more enjoyable for everyone. Thank you for taking the time to contribute! 🎄✨
