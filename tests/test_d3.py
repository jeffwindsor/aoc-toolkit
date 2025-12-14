"""Tests for 3D coordinate and grid functionality (d3 module)."""

import unittest
from aoc.d3 import Coord, Dimension, Grid


class TestCoord3D(unittest.TestCase):
    """Tests for 3D Coord class."""

    def test_creation(self):
        """Test 3D Coord creation."""
        coord = Coord(1, 2, 3)
        self.assertEqual(coord.x, 1)
        self.assertEqual(coord.y, 2)
        self.assertEqual(coord.z, 3)

    def test_addition(self):
        """Test 3D coordinate addition."""
        c1 = Coord(1, 2, 3)
        c2 = Coord(4, 5, 6)
        result = c1 + c2
        self.assertEqual(result, Coord(5, 7, 9))

    def test_subtraction(self):
        """Test 3D coordinate subtraction."""
        c1 = Coord(5, 8, 10)
        c2 = Coord(2, 3, 4)
        result = c1 - c2
        self.assertEqual(result, Coord(3, 5, 6))

    def test_manhattan_distance(self):
        """Test 3D Manhattan distance."""
        c1 = Coord(0, 0, 0)
        c2 = Coord(3, 4, 5)
        self.assertEqual(c1.manhattan_distance(c2), 12)

        c3 = Coord(-1, -2, -3)
        c4 = Coord(1, 2, 3)
        self.assertEqual(c3.manhattan_distance(c4), 12)

    def test_squared_distance(self):
        """Test 3D squared distance."""
        c1 = Coord(0, 0, 0)
        c2 = Coord(3, 4, 0)
        self.assertEqual(c1.squared_distance(c2), 25)

        c3 = Coord(1, 2, 2)
        c4 = Coord(4, 6, 2)
        self.assertEqual(c3.squared_distance(c4), 25)

    def test_euclidean_distance(self):
        """Test 3D Euclidean distance."""
        c1 = Coord(0, 0, 0)
        c2 = Coord(3, 4, 0)
        self.assertAlmostEqual(c1.euclidean_distance(c2), 5.0)

    def test_in_bounds(self):
        """Test 3D bounds checking."""
        coord = Coord(5, 5, 5)
        max_bounds = Coord(10, 10, 10)

        self.assertTrue(coord.in_bounds(max_bounds))
        self.assertTrue(Coord(0, 0, 0).in_bounds(max_bounds))
        self.assertTrue(Coord(10, 10, 10).in_bounds(max_bounds))
        self.assertFalse(Coord(-1, 5, 5).in_bounds(max_bounds))
        self.assertFalse(Coord(5, 11, 5).in_bounds(max_bounds))
        self.assertFalse(Coord(5, 5, 11).in_bounds(max_bounds))

    def test_in_bounds_with_min_bounds(self):
        """Test 3D bounds checking with custom min bounds."""
        coord = Coord(5, 5, 5)
        min_bounds = Coord(2, 2, 2)
        max_bounds = Coord(10, 10, 10)

        self.assertTrue(coord.in_bounds(max_bounds, min_bounds))
        self.assertFalse(Coord(1, 5, 5).in_bounds(max_bounds, min_bounds))
        self.assertFalse(Coord(5, 1, 5).in_bounds(max_bounds, min_bounds))
        self.assertFalse(Coord(5, 5, 1).in_bounds(max_bounds, min_bounds))

    def test_neighbors_cardinal(self):
        """Test getting 6 cardinal neighbors in 3D."""
        coord = Coord(5, 5, 5)
        max_bounds = Coord(10, 10, 10)
        neighbors = coord.neighbors(max_bounds)

        self.assertEqual(len(neighbors), 6)
        self.assertIn(Coord(5, 4, 5), neighbors)  # UP
        self.assertIn(Coord(5, 6, 5), neighbors)  # DOWN
        self.assertIn(Coord(4, 5, 5), neighbors)  # LEFT
        self.assertIn(Coord(6, 5, 5), neighbors)  # RIGHT
        self.assertIn(Coord(5, 5, 4), neighbors)  # BACK
        self.assertIn(Coord(5, 5, 6), neighbors)  # FORWARD

    def test_neighbors_at_edge(self):
        """Test 3D neighbors at grid edge."""
        coord = Coord(0, 0, 0)
        max_bounds = Coord(10, 10, 10)
        neighbors = coord.neighbors(max_bounds)

        # Only 3 neighbors: RIGHT, DOWN, FORWARD
        self.assertEqual(len(neighbors), 3)
        self.assertIn(Coord(1, 0, 0), neighbors)
        self.assertIn(Coord(0, 1, 0), neighbors)
        self.assertIn(Coord(0, 0, 1), neighbors)

    def test_direction_constants(self):
        """Test 3D direction constants."""
        self.assertEqual(Coord.ZERO, Coord(0, 0, 0))
        self.assertEqual(Coord.UP, Coord(0, -1, 0))
        self.assertEqual(Coord.DOWN, Coord(0, 1, 0))
        self.assertEqual(Coord.LEFT, Coord(-1, 0, 0))
        self.assertEqual(Coord.RIGHT, Coord(1, 0, 0))
        self.assertEqual(Coord.FORWARD, Coord(0, 0, 1))
        self.assertEqual(Coord.BACK, Coord(0, 0, -1))

    def test_directions_cardinal(self):
        """Test DIRECTIONS_CARDINAL contains all 6 directions."""
        self.assertEqual(len(Coord.DIRECTIONS_CARDINAL), 6)
        self.assertIn(Coord.UP, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.DOWN, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.LEFT, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.RIGHT, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.FORWARD, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.BACK, Coord.DIRECTIONS_CARDINAL)


class TestDimension3D(unittest.TestCase):
    """Tests for 3D Dimension class."""

    def test_creation(self):
        """Test 3D Dimension creation."""
        dim = Dimension(10, 5, 8)
        self.assertEqual(dim.width, 10)
        self.assertEqual(dim.height, 5)
        self.assertEqual(dim.depth, 8)


class TestGrid3D(unittest.TestCase):
    """Tests for 3D Grid class."""

    def test_creation(self):
        """Test 3D Grid creation."""
        # 2x2x2 cube
        data = [[['A', 'B'], ['C', 'D']], [['E', 'F'], ['G', 'H']]]
        grid = Grid(data)
        self.assertEqual(grid.size.width, 2)
        self.assertEqual(grid.size.height, 2)
        self.assertEqual(grid.size.depth, 2)

    def test_create_filled(self):
        """Test 3D Grid.create factory method."""
        grid = Grid.create(Dimension(3, 2, 2), '.')
        self.assertEqual(grid.size.width, 3)
        self.assertEqual(grid.size.height, 2)
        self.assertEqual(grid.size.depth, 2)
        self.assertEqual(grid[Coord(0, 0, 0)], '.')
        self.assertEqual(grid[Coord(2, 1, 1)], '.')

    def test_getitem(self):
        """Test 3D grid indexing with Coord."""
        data = [[['A', 'B'], ['C', 'D']], [['E', 'F'], ['G', 'H']]]
        grid = Grid(data)

        self.assertEqual(grid[Coord(0, 0, 0)], 'A')
        self.assertEqual(grid[Coord(1, 0, 0)], 'B')
        self.assertEqual(grid[Coord(0, 1, 0)], 'C')
        self.assertEqual(grid[Coord(1, 1, 0)], 'D')
        self.assertEqual(grid[Coord(0, 0, 1)], 'E')
        self.assertEqual(grid[Coord(1, 0, 1)], 'F')
        self.assertEqual(grid[Coord(0, 1, 1)], 'G')
        self.assertEqual(grid[Coord(1, 1, 1)], 'H')

    def test_setitem(self):
        """Test 3D grid assignment with Coord."""
        data = [[['A', 'B'], ['C', 'D']], [['E', 'F'], ['G', 'H']]]
        grid = Grid(data)

        grid[Coord(1, 0, 0)] = 'X'
        self.assertEqual(grid[Coord(1, 0, 0)], 'X')

    def test_contains(self):
        """Test 3D bounds checking with 'in' operator."""
        data = [[['A', 'B'], ['C', 'D']], [['E', 'F'], ['G', 'H']]]
        grid = Grid(data)

        self.assertTrue(Coord(0, 0, 0) in grid)
        self.assertTrue(Coord(1, 1, 1) in grid)
        self.assertFalse(Coord(2, 2, 2) in grid)
        self.assertFalse(Coord(-1, 0, 0) in grid)

    def test_max_bounds(self):
        """Test 3D max_bounds property."""
        data = [[['A', 'B', 'C'], ['D', 'E', 'F']], [['G', 'H', 'I'], ['J', 'K', 'L']]]
        grid = Grid(data)
        max_bounds = grid.max_bounds

        self.assertEqual(max_bounds.x, 2)
        self.assertEqual(max_bounds.y, 1)
        self.assertEqual(max_bounds.z, 1)

    def test_coords_iterator(self):
        """Test 3D coords iterator."""
        data = [[['A', 'B'], ['C', 'D']], [['E', 'F'], ['G', 'H']]]
        grid = Grid(data)
        coords_values = list(grid.coords())

        self.assertEqual(len(coords_values), 8)
        coords = [coord for coord, _ in coords_values]
        self.assertIn(Coord(0, 0, 0), coords)
        self.assertIn(Coord(1, 1, 1), coords)


if __name__ == '__main__':
    unittest.main()
