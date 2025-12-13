"""
Advent of Code 2024 Utilities

Organized into modules but accessible from top level for convenience:
- d2: 2D coordinate and grid operations
- d3: 3D coordinate and grid operations (explicit import required)
- graph: Graph algorithms (BFS, DFS, Dijkstra, max clique, flood fill, path counting)
- input: Data reading and parsing (Input and Parser classes)
- math: Number/math utilities
- testing: Test framework

Import styles supported:
    # Simple (recommended for puzzles)
    from aoc import Coord, Grid, bfs, Input, run, TestCase

    # Explicit 2D (optional for clarity)
    from aoc.d2 import Coord, Grid, Dimension

    # Explicit 3D (required for 3D types)
    from aoc.d3 import Coord, Grid, Dimension
"""

# Re-export everything for backward compatibility
from .d2 import *
from .graph import *
from .input import *
from .math import *
from .testing import *

# Explicit __all__ for clarity
__all__ = [
    # From d2 (default for 2D operations)
    "Coord",
    "Dimension",
    "filter_coords_in_bounds",
    "Grid",
    # From graph
    "bfs",
    "dfs",
    "bfs_grid_path",
    "dfs_grid_path",
    "flood_fill",
    "flood_fill_mark",
    "dijkstra",
    "count_paths_dag",
    "count_paths_cyclic",
    "find_max_clique",
    "UnionFind",
    # From input
    "Input",
    "extract_ints",
    "extract_pattern",
    "pattern_to_bools",
    "extract_bracketed",
    "extract_parenthesized",
    "extract_braced",
    # From math
    "count_continuous_segments",
    "count_digits",
    "calculate_toggle_states",
    # From testing
    "TestCase",
    "run",
]
