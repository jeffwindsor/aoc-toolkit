"""
AOC Solution Template - Copy this to start your solution

This template shows the recommended structure for solving Advent of Code puzzles
using aoc-toolkit. Copy this file and modify it for your specific puzzle.

File structure:
  your_solution/
  ├── solution.py          # This file
  └── data/
      ├── example_01       # Example input from puzzle description
      ├── example_01.part1.answer  # Expected result for example (optional)
      ├── example_01.part2.answer  # Expected result for example (optional)
      ├── puzzle_input     # Your actual puzzle input
      ├── puzzle_input.part1.answer  # Your answer for part 1 (optional)
      └── puzzle_input.part2.answer  # Your answer for part 2 (optional)

Answer files are optional but recommended - the test runner will automatically
load expected values from these files if they exist.
"""

from aoc import (
    # Data I/O - choose what you need
    read_data_as_lines,      # Most common - list of strings
    read_data_as_char_grid,  # For grid-based puzzles
    read_data_as_int_grid,   # For numeric grids
    read_data_as_ints,       # List of integers (one per line)
    read_data_as_coord_pairs,  # Parse coordinate pairs
    read_data_as_graph_edges,  # Parse graph connections
    # Testing
    run, TestCase,
    # Add other imports as needed:
    # Coord, grid_get, find_first, bfs, dijkstra, etc.
)


def solve_part1(data_file: str) -> int:
    """
    Solve part 1 of the puzzle.

    Args:
        data_file: Name of the data file in ./data/ directory

    Returns:
        Solution to part 1
    """
    # Read the input data
    lines = read_data_as_lines(data_file)

    # Your solution code here
    result = 0

    return result


def solve_part2(data_file: str) -> int:
    """
    Solve part 2 of the puzzle.

    Args:
        data_file: Name of the data file in ./data/ directory

    Returns:
        Solution to part 2
    """
    # Read the input data
    lines = read_data_as_lines(data_file)

    # Your solution code here
    result = 0

    return result


if __name__ == "__main__":
    # Part 1
    print("=" * 50)
    print("Part 1")
    print("=" * 50)
    run(solve_part1, [
        TestCase("example_01"),      # Run with example input first
        TestCase("puzzle_input"),    # Then run with your puzzle input
    ], part="part1")

    # Part 2
    print("\n" + "=" * 50)
    print("Part 2")
    print("=" * 50)
    run(solve_part2, [
        TestCase("example_01"),
        TestCase("puzzle_input"),
    ], part="part2")


# ==============================================================================
# Common Patterns - Uncomment and adapt as needed
# ==============================================================================

# # Grid-based puzzle pattern:
# def solve_grid_puzzle(data_file: str) -> int:
#     from aoc import Coord, find_first, grid_max_bounds
#
#     grid = read_data_as_char_grid(data_file)
#     start = find_first(grid, 'S')
#     max_bounds = grid_max_bounds(grid)
#
#     # Your grid navigation logic here
#     return 0


# # Shortest path pattern:
# def solve_shortest_path(data_file: str) -> int:
#     from aoc import bfs, Coord
#
#     grid = read_data_as_char_grid(data_file)
#
#     def neighbors(pos):
#         # Return list of valid neighbor positions
#         return []
#
#     distances = bfs(start, neighbors)
#     return distances[goal]


# # Graph pattern:
# def solve_graph(data_file: str) -> int:
#     from aoc import dijkstra
#
#     edges = read_data_as_graph_edges(data_file)
#
#     def weighted_neighbors(node):
#         # Return [(neighbor, cost), ...] for each node
#         return [(n, 1) for n in edges.get(node, [])]
#
#     distances = dijkstra('START', weighted_neighbors)
#     return distances['END']
