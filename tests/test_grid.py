"""Tests for grid module."""

import unittest
from aoc import (
    Coord,
    grid_size,
    grid_max_bounds,
    grid_contains_coord,
    grid_get,
    grid_set,
    find_first,
    find_all,
    grid_coords,
    create_grid,
)


class TestGrid(unittest.TestCase):
    """Test grid operations."""

    def setUp(self):
        """Set up test grid."""
        self.grid = [
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I']
        ]

    def test_grid_size(self):
        """Test grid size calculation."""
        size = grid_size(self.grid)
        self.assertEqual(size, Coord(3, 3))

    def test_grid_max_bounds(self):
        """Test max bounds calculation."""
        bounds = grid_max_bounds(self.grid)
        self.assertEqual(bounds, Coord(2, 2))

    def test_grid_contains_coord(self):
        """Test coordinate containment check."""
        self.assertTrue(grid_contains_coord(self.grid, Coord(0, 0)))
        self.assertTrue(grid_contains_coord(self.grid, Coord(2, 2)))
        self.assertFalse(grid_contains_coord(self.grid, Coord(3, 3)))
        self.assertFalse(grid_contains_coord(self.grid, Coord(-1, 0)))

    def test_grid_get(self):
        """Test getting value from grid."""
        self.assertEqual(grid_get(self.grid, Coord(0, 0)), 'A')
        self.assertEqual(grid_get(self.grid, Coord(1, 1)), 'E')
        self.assertEqual(grid_get(self.grid, Coord(2, 2)), 'I')
        # Out of bounds raises IndexError
        with self.assertRaises(IndexError):
            grid_get(self.grid, Coord(5, 5))

    def test_grid_set(self):
        """Test setting value in grid."""
        test_grid = [row[:] for row in self.grid]  # Deep copy
        grid_set(test_grid, Coord(1, 1), 'X')
        self.assertEqual(grid_get(test_grid, Coord(1, 1)), 'X')

    def test_find_first(self):
        """Test finding first occurrence."""
        pos = find_first(self.grid, 'E')
        self.assertEqual(pos, Coord(1, 1))

        not_found = find_first(self.grid, 'Z')
        self.assertIsNone(not_found)

    def test_find_all(self):
        """Test finding all occurrences."""
        grid_with_duplicates = [
            ['A', 'X', 'C'],
            ['X', 'E', 'F'],
            ['G', 'X', 'I']
        ]
        positions = find_all(grid_with_duplicates, 'X')
        self.assertEqual(len(positions), 3)
        self.assertIn(Coord(0, 1), positions)
        self.assertIn(Coord(1, 0), positions)
        self.assertIn(Coord(2, 1), positions)

    def test_grid_coords(self):
        """Test iterating over grid coordinates."""
        coords = list(grid_coords(self.grid))
        self.assertEqual(len(coords), 9)

        # Check first and last
        self.assertEqual(coords[0], (Coord(0, 0), 'A'))
        self.assertEqual(coords[-1], (Coord(2, 2), 'I'))

    def test_create_grid(self):
        """Test creating a new grid."""
        # create_grid takes size (int) and creates square grid
        grid = create_grid(3, initial_value='.')
        self.assertEqual(len(grid), 3)
        self.assertEqual(len(grid[0]), 3)
        self.assertEqual(grid[0][0], '.')
        self.assertEqual(grid[2][2], '.')


if __name__ == "__main__":
    unittest.main()
