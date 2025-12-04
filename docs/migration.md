# Migration Guide

[← Back to README](../README.md)

Quick guide for migrating existing Advent of Code projects to aoc-toolkit.

## Table of Contents

- [Quick Migration](#quick-migration)
- [Detailed Migration](#detailed-migration)
- [Custom Adaptations](#custom-adaptations)
- [Upgrading](#upgrading)

---

## Quick Migration

**If you have a compatible local `aoc/` package:**

```bash
# 1. Install
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0

# 2. Add to requirements.txt
echo "aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0" > requirements.txt

# 3. Test one solution
python3 solution.py

# 4. Remove local package (if tests pass)
rm -rf aoc/
```

**If imports match (`from aoc import ...`), you're done!**

---

## Detailed Migration

### Prerequisites

- Python 3.10+
- Git repository (recommended for safety)
- Backup current work: `git commit -m "Checkpoint before migration"`

### Step-by-Step Process

#### 1. Install and Verify

```bash
# Install
pip install git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0

# Verify
python3 -c "from aoc import read_data, Coord, bfs; print('Success!')"
```

#### 2. Test With Local Package Still Present

```bash
# Test one solution - both packages available
python3 01_solution.py
```

If successful, imports are using the new toolkit.

#### 3. Remove Local Package

```bash
rm -rf aoc/
```

#### 4. Add Dependency Management

**requirements.txt:**
```
aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0
```

**Or pyproject.toml:**
```toml
[project]
dependencies = [
    "aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0"
]
```

#### 5. Test Everything

```bash
# Run all solutions
for file in ??_*.py; do
    python3 "$file" || echo "FAILED: $file"
done
```

#### 6. Commit Changes

```bash
git add requirements.txt
git rm -r aoc/  # If not already removed
git commit -m "Migrate to aoc-toolkit v1.0.0"
```

### Compatibility Check

Your local package is compatible if:
- ✓ Imports work: `from aoc import read_data, Coord, bfs, run, TestCase`
- ✓ Data files in: `./data/{filename}` (no extension)
- ✓ Answer files: `./data/{filename}.{part}.answer`

Not compatible if:
- ✗ Different import paths: `from utils import ...`
- ✗ Different data file locations
- ✗ Custom test runner with different API

### Refactoring from Scratch

**If you have no package or incompatible patterns:**

**Before:**
```python
def solve(filename):
    with open(f"data/{filename}") as f:
        lines = f.read().strip().split('\n')
    grid = [list(line) for line in lines]

    # Find start manually
    start = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
                break
    return result

if __name__ == "__main__":
    assert solve("example") == 42
    print(f"Answer: {solve('input')}")
```

**After:**
```python
from aoc import read_data_as_char_grid, find_first, run, TestCase

def solve(data_file):
    grid = read_data_as_char_grid(data_file)
    start = find_first(grid, 'S')
    return result

if __name__ == "__main__":
    run(solve, [
        TestCase("example"),  # Answer in data/example.part1.answer
        TestCase("input"),
    ], part="part1")
```

Create answer files:
```bash
echo "42" > data/example.part1.answer
```

---

## Custom Adaptations

### Different Import Names

**Option 1: Alias imports**
```python
from aoc import read_data_as_lines as read_lines
```

**Option 2: Wrapper module**
```python
# utils.py
from aoc import read_data_as_lines as read_lines, Coord as Point
```

Keep old imports in solutions:
```python
from utils import read_lines, Point
```

### Different Data Directory

**Symlink approach:**
```bash
ln -s actual_data_directory data
```

**Or use environment variable:**
```python
import os
os.chdir(DATA_DIR)  # Before importing aoc
```

### Custom Utilities

Keep custom utilities separate:
```
your_project/
├── custom_utils.py   # Your custom functions
└── solutions/
```

```python
from aoc import read_data_as_lines, Coord  # From toolkit
from custom_utils import your_function      # Your custom code
```

---

## Upgrading

### Check Current Version

```bash
pip show aoc-toolkit | grep Version
```

### Upgrade Process

```bash
# 1. Update requirements.txt
# Change: @v1.0.0 to @v1.1.0

# 2. Reinstall
pip install --upgrade git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.1.0

# 3. Test
python3 01_solution.py

# 4. Commit
git add requirements.txt
git commit -m "Upgrade aoc-toolkit to v1.1.0"
```

### Version Compatibility

- **1.0.x → 1.y.z**: Safe, no breaking changes
- **1.x → 2.0**: Review [changelog](https://github.com/jeffwindsor/aoc-toolkit/releases) for breaking changes

---

## Rollback

If migration fails:

```bash
# Uninstall toolkit
pip uninstall aoc-toolkit

# Restore from git
git reset --hard HEAD~1

# Or restore local package
git checkout HEAD~1 -- aoc/
```

---

## Tips

### Version Pinning
```
# Good - reproducible
aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git@v1.0.0

# Bad - unstable
aoc-toolkit @ git+https://github.com/jeffwindsor/aoc-toolkit.git
```

### Gitignore
```gitignore
# Exclude puzzle inputs and answers
data/*puzzle_input*
data/*.answer

# Keep examples
!data/*example*
```

### Migration Test Script
```bash
#!/bin/bash
# test_migration.sh

# Test imports
python3 -c "from aoc import read_data, Coord, bfs, run, TestCase" || exit 1
echo "✓ Imports work"

# Test solutions
for day in {1..25}; do
    file=$(printf "%02d_*.py" $day)
    [ -f "$file" ] && python3 "$file"
done

echo "✓ Migration complete"
```

---

[← Back to README](../README.md)
