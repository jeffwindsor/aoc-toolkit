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

The toolkit supports three import styles:

```python
# Flat imports (recommended for convenience)
from aoc import Coord, bfs, run, TestCase

# Explicit module imports (recommended for clarity)
from aoc.coord import Coord
from aoc.graph import bfs

# Namespace imports
import aoc
import aoc.coord
import aoc.graph
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
