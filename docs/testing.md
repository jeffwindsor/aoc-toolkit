# Testing Framework

[← Back to README](../README.md)

The `aoc.testing` module provides a simple test runner with colored output, answer file management, and optional performance metrics.

## Table of Contents

- [Quick Start](#quick-start)
- [TestCase Class](#testcase-class)
- [run() Function](#run-function)
- [Answer Files](#answer-files)
- [Performance Metrics](#performance-metrics)
- [Examples](#examples)

## Quick Start

```python
from aoc import run, TestCase

def solve(data_file):
    # Your solution here
    return result

if __name__ == "__main__":
    run(solve, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part1")
```

## TestCase Class

```python
from dataclasses import dataclass

@dataclass
class TestCase:
    data_file: str
    expected: Any = None
```

**Parameters:**
- `data_file`: Filename in `./data/` directory (without path)
- `expected`: Expected result (optional, loads from answer file if not provided)

**Examples:**
```python
# Load expected from answer file
TestCase("example_01")

# Explicit expected value (overrides answer file)
TestCase("example_01", 42)
TestCase("puzzle_input", "answer")
TestCase("test_data", [1, 2, 3])
```

## run() Function

```python
def run(
    func: Callable[[str], Any],
    test_cases: list[TestCase],
    part: str | None = None
) -> None
```

Executes test cases and displays results with colored output.

**Parameters:**
- `func`: Solution function that takes `data_file` and returns a result
- `test_cases`: List of TestCase instances
- `part`: Part identifier for answer file lookup ("part1", "part2", etc.)

**Output Format:**
```
solve_part1
  ✓ example_01: 42 (120.5 µs, 1.2 KB)  # Green for pass
  ✗ puzzle_input: expected 100, got 99  # Red for fail

2 tests: 1 passed, 1 failed
```

**Color Codes:**
- **Green**: Test passed
- **Red**: Test failed
- **Blue**: Function name header

## Answer Files

### Convention

Answer files are stored alongside data files with `.{part}.answer` extension:

```
data/
├── example_01                  # Input data
├── example_01.part1.answer     # Part 1 expected answer
├── example_01.part2.answer     # Part 2 expected answer
├── puzzle_input
├── puzzle_input.part1.answer
└── puzzle_input.part2.answer
```

### Loading Behavior

```python
# Automatic loading (requires part parameter)
run(solve, [TestCase("example_01")], part="part1")
# Looks for: data/example_01.part1.answer

# Explicit value overrides answer file
run(solve, [TestCase("example_01", 42)], part="part1")
# Uses 42, ignores answer file

# Mixed approach
run(solve, [
    TestCase("example_01", 42),  # Explicit
    TestCase("puzzle_input"),    # From answer file
], part="part1")
```

### Answer File Format

Answer files contain a single value (no trailing newline):

**Integer:**
```
42
```

**String:**
```
ANSWER
```

**Float:**
```
3.14
```

### Type Conversion

The loader attempts conversions in order:
1. **Integer**: `int(content)`
2. **Float**: `float(content)` if int fails
3. **String**: Raw content if both fail

```python
# answer file: "42"      → int: 42
# answer file: "3.14"    → float: 3.14
# answer file: "HELLO"   → str: "HELLO"
```

### Missing Answer Files

If answer file doesn't exist and `expected` is None:
```
⚠ example_01: No expected value (provide expected or create answer file)
```

Test is skipped but not marked as failure.

## Performance Metrics

### Enabling Metrics

Create `.aoc_config` file in project root:

```bash
# Enable
echo "test_performance_tracking=true" > .aoc_config

# Disable
echo "test_performance_tracking=false" > .aoc_config

# Or delete file (defaults to disabled)
rm .aoc_config
```

### Output With Metrics

```
solve_part1
  ✓ example_01: 42 (120.5 µs, 1.2 KB)
  ✓ puzzle_input: 1234 (3.2 ms, 45.3 KB)
```

**Format:**
- **Time**: Displays as µs/ms/s depending on magnitude
- **Memory**: Displays as B/KB/MB

### Time Thresholds

- **< 1 µs**: Shows microseconds (µs)
- **1 µs - 1 ms**: Shows microseconds (µs)
- **1 ms - 1 s**: Shows milliseconds (ms)
- **≥ 1 s**: Shows seconds (s)

### Memory Thresholds

- **< 1 KB**: Shows bytes (B)
- **1 KB - 1 MB**: Shows kilobytes (KB)
- **≥ 1 MB**: Shows megabytes (MB)

### Performance Tips

- Metrics measure only solution function execution (not file I/O)
- Memory tracks peak delta during function execution
- Cached at module import for zero per-test overhead
- Disable for faster test runs when not optimizing

## Examples

### Basic Usage

```python
from aoc import run, TestCase

def solve_part1(data_file):
    # Implementation
    return 42

def solve_part2(data_file):
    # Implementation
    return "ANSWER"

if __name__ == "__main__":
    # Part 1 tests
    run(solve_part1, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part1")

    # Part 2 tests
    run(solve_part2, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part2")
```

### Explicit Expected Values

```python
# Override answer files for specific tests
run(solve, [
    TestCase("example_01", 42),       # Explicit
    TestCase("example_02", 100),      # Explicit
    TestCase("puzzle_input"),         # From answer file
], part="part1")
```

### Multiple Test Files

```python
# Test against multiple examples
TESTS = [
    TestCase("example_01"),
    TestCase("example_02"),
    TestCase("example_03"),
    TestCase("puzzle_input"),
]

run(solve_part1, TESTS, part="part1")
run(solve_part2, TESTS, part="part2")
```

### Shared Test Configuration

```python
# Define tests once, reuse for both parts
TESTS = [
    TestCase("example_01"),
    TestCase("puzzle_input"),
]

if __name__ == "__main__":
    run(solve_part1, TESTS, part="part1")
    run(solve_part2, TESTS, part="part2")
```

### Development Workflow

```python
# During development: explicit values for quick iteration
run(solve, [
    TestCase("example_01", 42),
    # TestCase("puzzle_input"),  # Comment out until example passes
], part="part1")

# After solving: move to answer files
# 1. Create data/example_01.part1.answer with "42"
# 2. Create data/puzzle_input.part1.answer with actual answer
# 3. Update code:

run(solve, [
    TestCase("example_01"),      # Now loads from answer file
    TestCase("puzzle_input"),    # Now loads from answer file
], part="part1")
```

### Testing Edge Cases

```python
# Mix explicit and file-based expected values
run(solve, [
    TestCase("empty_input", 0),           # Edge case: explicit
    TestCase("single_item", 1),           # Edge case: explicit
    TestCase("example_01"),               # Normal: from file
    TestCase("puzzle_input"),             # Normal: from file
], part="part1")
```

## Best Practices

### Answer File Strategy

**Recommended (cleaner scripts):**
```python
# Answer files: data/example_01.part1.answer
run(solve, [TestCase("example_01")], part="part1")
```

**Alternative (self-contained):**
```python
# Explicit values in code
run(solve, [TestCase("example_01", 42)], part="part1")
```

### Test Organization

```python
# Clear structure with comments
if __name__ == "__main__":
    # Part 1: Find shortest path
    run(solve_part1, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part1")

    # Part 2: Find longest path
    run(solve_part2, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part2")
```

### Performance Optimization

```python
# Enable metrics during optimization
# .aoc_config: test_performance_tracking=true

run(solve_optimized, [
    TestCase("example_01"),      # Should be <1ms
    TestCase("large_input"),     # Should be <10ms
], part="part1")

# Disable after optimization complete
# .aoc_config: test_performance_tracking=false
```

### Gitignore Pattern

Add to `.gitignore` to exclude puzzle inputs and answers:
```gitignore
data/*puzzle_input*
data/*.answer
```

Keep example inputs and answers in version control:
```gitignore
data/*puzzle_input*
data/*puzzle_input*.answer
```

---

[← Back to README](../README.md) | [Next: Coordinates →](coordinates.md)
