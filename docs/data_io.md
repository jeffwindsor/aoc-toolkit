# Data I/O Module

[← Back to README](../README.md)

The `aoc.data` module provides specialized functions for reading and parsing Advent of Code puzzle inputs. All functions expect files in the `./data/` directory relative to your script.

## Table of Contents

- [Basic Reading](#basic-reading)
- [Line-Based Input](#line-based-input)
- [Grid Input](#grid-input)
- [Structured Data](#structured-data)
- [Text Parsing](#text-parsing)
- [Function Reference](#function-reference)

## Basic Reading

### `read_data(data_file: str) -> str`

Reads entire file as raw string.

**Parameters:**
- `data_file`: Filename (without path, no extension)

**Returns:** Raw file contents as string

**Example:**
```python
from aoc import read_data

content = read_data("puzzle_input")
# "line 1\nline 2\n...
```

**Use when:** You need full control over parsing, or for single-value inputs.

## Line-Based Input

### `read_data_as_lines(data_file: str, strip_whitespace: bool = True) -> list[str]`

Reads file as list of lines.

**Parameters:**
- `data_file`: Filename
- `strip_whitespace`: Remove leading/trailing whitespace (default: True)

**Returns:** List of strings (one per line)

**Example:**
```python
from aoc import read_data_as_lines

lines = read_data_as_lines("input")
# ['instruction 1', 'instruction 2', ...]

# Preserve whitespace
lines = read_data_as_lines("input", strip_whitespace=False)
# ['  instruction 1  \n', '  instruction 2  \n', ...]
```

**Use when:** Each line represents a separate item (instructions, rules, etc.).

### `read_data_as_ints(data_file: str) -> list[int]`

Reads file as list of integers (one per line).

**Parameters:**
- `data_file`: Filename

**Returns:** List of integers

**Example:**
```python
from aoc import read_data_as_ints

numbers = read_data_as_ints("heights")
# [120, 125, 118, ...]
```

**Use when:** Input is a list of numbers, one per line.

## Grid Input

### `read_data_as_char_grid(data_file: str) -> list[list[str]]`

Reads file as 2D character grid.

**Parameters:**
- `data_file`: Filename

**Returns:** 2D list of single characters

**Example:**
```python
from aoc import read_data_as_char_grid

# File content:
# #.#
# .S.
# #.#

grid = read_data_as_char_grid("maze")
# [['#', '.', '#'],
#  ['.', 'S', '.'],
#  ['#', '.', '#']]

# Access cell
cell = grid[1][1]  # 'S'
```

**Use when:** Parsing maps, mazes, or any 2D character layout.

### `read_data_as_int_grid(data_file: str, empty_value: int = -1) -> list[list[int]]`

Reads file as 2D integer grid.

**Parameters:**
- `data_file`: Filename
- `empty_value`: Value for non-digit characters (default: -1)

**Returns:** 2D list of integers

**Example:**
```python
from aoc import read_data_as_int_grid

# File content:
# 123
# 456
# 789

grid = read_data_as_int_grid("heights")
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]

# With non-digit handling
# File: "1.3"
grid = read_data_as_int_grid("sparse", empty_value=0)
# [[1, 0, 3]]
```

**Use when:** Parsing height maps, distance grids, or numeric 2D data.

## Structured Data

### `read_data_as_coord_pairs(data_file: str, separator: str = ",") -> list[tuple[int, int]]`

Reads file as list of coordinate pairs.

**Parameters:**
- `data_file`: Filename
- `separator`: Delimiter between coordinates (default: ",")

**Returns:** List of (x, y) tuples

**Example:**
```python
from aoc import read_data_as_coord_pairs

# File content:
# 3,4
# 1,2
# 5,0

coords = read_data_as_coord_pairs("positions")
# [(3, 4), (1, 2), (5, 0)]

# Custom separator
# File: "3:4\n1:2"
coords = read_data_as_coord_pairs("positions", separator=":")
# [(3, 4), (1, 2)]
```

**Use when:** Parsing positions, points, or coordinate lists.

### `read_data_as_graph_edges(data_file: str, separator: str = "-", directed: bool = False) -> dict[str, set[str]]`

Reads file as adjacency list graph.

**Parameters:**
- `data_file`: Filename
- `separator`: Delimiter between nodes (default: "-")
- `directed`: Create directed graph (default: False for undirected)

**Returns:** Adjacency dictionary `{node: {neighbors}}`

**Example:**
```python
from aoc import read_data_as_graph_edges

# File content:
# A-B
# B-C
# C-A

graph = read_data_as_graph_edges("connections")
# {
#     'A': {'B', 'C'},
#     'B': {'A', 'C'},
#     'C': {'B', 'A'}
# }

# Directed graph
graph = read_data_as_graph_edges("connections", directed=True)
# {
#     'A': {'B'},
#     'B': {'C'},
#     'C': {'A'}
# }
```

**Use when:** Parsing network connections, relationships, or graph structures.

### `read_data_as_sections(data_file: str, strip: bool = True) -> list[str]`

Splits file into sections separated by blank lines.

**Parameters:**
- `data_file`: Filename
- `strip`: Strip whitespace from sections (default: True)

**Returns:** List of section strings

**Example:**
```python
from aoc import read_data_as_sections

# File content:
# section 1
# more data
#
# section 2
# other data

sections = read_data_as_sections("multi_part")
# ['section 1\nmore data', 'section 2\nother data']

# Process each section
for section in sections:
    lines = section.split('\n')
    # Process lines...
```

**Use when:** Input has multiple distinct sections (rules + data, header + body, etc.).

### `read_data_as_columns(data_file: str, separator: str | None = None, converter: type = int) -> list[list]`

Reads columnar data and transposes to column lists.

**Parameters:**
- `data_file`: Filename
- `separator`: Column delimiter (default: None for whitespace)
- `converter`: Type conversion function (default: int)

**Returns:** List of columns (each column is a list)

**Example:**
```python
from aoc import read_data_as_columns

# File content:
# 1 2 3
# 4 5 6
# 7 8 9

columns = read_data_as_columns("table")
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

col1, col2, col3 = columns
# col1 = [1, 4, 7]
# col2 = [2, 5, 8]
# col3 = [3, 6, 9]

# String columns
columns = read_data_as_columns("names", converter=str)
# [['Alice', 'Bob'], ['123', '456'], ...]
```

**Use when:** Working with tabular data where you need columns (not rows).

## Text Parsing

### `extract_ints(text: str) -> list[int]`

Extracts all integers (including negatives) from text.

**Parameters:**
- `text`: Input string

**Returns:** List of integers found in text

**Example:**
```python
from aoc import extract_ints

nums = extract_ints("p=3,4 v=-2,5")
# [3, 4, -2, 5]

nums = extract_ints("Move 10 units, rotate -45 degrees")
# [10, -45]

# Use with read_data for complex parsing
from aoc import read_data
text = read_data("complex_input")
all_numbers = extract_ints(text)
```

**Use when:** Input mixes numbers with text, or has irregular number formats.

## Function Reference

### Summary Table

| Function | Input Format | Output Type | Common Use Cases |
|----------|--------------|-------------|------------------|
| `read_data` | Any text | `str` | Full control, single values |
| `read_data_as_lines` | Line-per-item | `list[str]` | Instructions, rules, lists |
| `read_data_as_ints` | Integer-per-line | `list[int]` | Number lists, measurements |
| `read_data_as_char_grid` | 2D characters | `list[list[str]]` | Maps, mazes, layouts |
| `read_data_as_int_grid` | 2D digits | `list[list[int]]` | Height maps, distance grids |
| `read_data_as_coord_pairs` | "x,y" pairs | `list[tuple[int, int]]` | Positions, points |
| `read_data_as_graph_edges` | "node-node" | `dict[str, set[str]]` | Networks, connections |
| `read_data_as_sections` | Multi-section | `list[str]` | Grouped input data |
| `read_data_as_columns` | Tabular | `list[list]` | Column-oriented data |
| `extract_ints` | Mixed text | `list[int]` | Irregular number formats |

### Data File Convention

All functions expect files in `./data/` directory:

```
your_project/
├── solution.py
└── data/
    ├── example_01
    ├── puzzle_input
    └── ...
```

**Usage:** Pass filename only (no path, no extension):
```python
data = read_data_as_lines("puzzle_input")  # Reads ./data/puzzle_input
```

## Tips & Best Practices

### Choose the Right Function

- **Simple list of items?** → `read_data_as_lines()`
- **2D grid/maze?** → `read_data_as_char_grid()` or `read_data_as_int_grid()`
- **Positions/coordinates?** → `read_data_as_coord_pairs()`
- **Graph/network?** → `read_data_as_graph_edges()`
- **Multiple sections?** → `read_data_as_sections()`
- **Complex mixed format?** → `read_data()` + custom parsing or `extract_ints()`

### Performance Considerations

- All functions read entire file into memory
- For very large files (>100MB), consider streaming with native Python `open()`
- Grid functions create nested lists (O(rows × cols) memory)

### Error Handling

Functions will raise `FileNotFoundError` if file doesn't exist:
```python
try:
    data = read_data_as_lines("missing_file")
except FileNotFoundError:
    print("File not found in ./data/ directory")
```

---

[← Back to README](../README.md) | [Next: Testing →](testing.md)
