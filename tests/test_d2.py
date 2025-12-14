"""Tests for 2D coordinate and grid functionality (d2 module)."""

import unittest
from aoc.d2 import Coord, Dimension, Grid, filter_coords_in_bounds


class TestCoord(unittest.TestCase):
    """Tests for 2D Coord class."""

    def test_creation_x_y(self):
        """Test Coord creation with x, y."""
        coord = Coord(3, 5)
        self.assertEqual(coord.x, 3)
        self.assertEqual(coord.y, 5)

    def test_creation_from_rc(self):
        """Test Coord.from_rc factory method."""
        coord = Coord.from_rc(row=5, col=3)
        self.assertEqual(coord.x, 3)
        self.assertEqual(coord.y, 5)
        self.assertEqual(coord.row, 5)
        self.assertEqual(coord.col, 3)

    def test_row_col_properties(self):
        """Test row and col properties."""
        coord = Coord(3, 5)
        self.assertEqual(coord.row, 5)  # row = y
        self.assertEqual(coord.col, 3)  # col = x

    def test_addition(self):
        """Test coordinate addition."""
        c1 = Coord(3, 5)
        c2 = Coord(1, 2)
        result = c1 + c2
        self.assertEqual(result, Coord(4, 7))

    def test_subtraction(self):
        """Test coordinate subtraction."""
        c1 = Coord(5, 8)
        c2 = Coord(2, 3)
        result = c1 - c2
        self.assertEqual(result, Coord(3, 5))

    def test_manhattan_distance(self):
        """Test Manhattan distance calculation."""
        c1 = Coord(0, 0)
        c2 = Coord(3, 4)
        self.assertEqual(c1.manhattan_distance(c2), 7)

        c3 = Coord(-2, -3)
        c4 = Coord(1, 2)
        self.assertEqual(c3.manhattan_distance(c4), 8)

    def test_euclidean_distance(self):
        """Test Euclidean distance calculation."""
        c1 = Coord(0, 0)
        c2 = Coord(3, 4)
        self.assertAlmostEqual(c1.euclidean_distance(c2), 5.0)

    def test_squared_distance(self):
        """Test squared distance calculation."""
        c1 = Coord(0, 0)
        c2 = Coord(3, 4)
        self.assertEqual(c1.squared_distance(c2), 25)

    def test_in_bounds(self):
        """Test bounds checking."""
        coord = Coord(5, 5)
        max_bounds = Coord(10, 10)

        self.assertTrue(coord.in_bounds(max_bounds))
        self.assertTrue(Coord(0, 0).in_bounds(max_bounds))
        self.assertTrue(Coord(10, 10).in_bounds(max_bounds))
        self.assertFalse(Coord(-1, 5).in_bounds(max_bounds))
        self.assertFalse(Coord(5, 11).in_bounds(max_bounds))

    def test_in_bounds_with_min_bounds(self):
        """Test bounds checking with custom min bounds."""
        coord = Coord(5, 5)
        min_bounds = Coord(2, 2)
        max_bounds = Coord(10, 10)

        self.assertTrue(coord.in_bounds(max_bounds, min_bounds))
        self.assertFalse(Coord(1, 5).in_bounds(max_bounds, min_bounds))

    def test_neighbors_cardinal(self):
        """Test getting cardinal neighbors."""
        coord = Coord(5, 5)
        max_bounds = Coord(10, 10)
        neighbors = coord.neighbors(max_bounds)

        self.assertEqual(len(neighbors), 4)
        self.assertIn(Coord(5, 4), neighbors)  # UP
        self.assertIn(Coord(6, 5), neighbors)  # RIGHT
        self.assertIn(Coord(5, 6), neighbors)  # DOWN
        self.assertIn(Coord(4, 5), neighbors)  # LEFT

    def test_neighbors_all_directions(self):
        """Test getting all 8 neighbors."""
        coord = Coord(5, 5)
        max_bounds = Coord(10, 10)
        neighbors = coord.neighbors(max_bounds, Coord.DIRECTIONS_ALL)

        self.assertEqual(len(neighbors), 8)

    def test_neighbors_at_edge(self):
        """Test neighbors at grid edge."""
        coord = Coord(0, 0)
        max_bounds = Coord(10, 10)
        neighbors = coord.neighbors(max_bounds)

        self.assertEqual(len(neighbors), 2)  # Only RIGHT and DOWN
        self.assertIn(Coord(1, 0), neighbors)
        self.assertIn(Coord(0, 1), neighbors)

    def test_direction_constants(self):
        """Test direction constants."""
        self.assertEqual(Coord.ZERO, Coord(0, 0))
        self.assertEqual(Coord.UP, Coord(0, -1))
        self.assertEqual(Coord.DOWN, Coord(0, 1))
        self.assertEqual(Coord.LEFT, Coord(-1, 0))
        self.assertEqual(Coord.RIGHT, Coord(1, 0))

    def test_turn_clockwise(self):
        """Test clockwise rotation."""
        self.assertEqual(Coord.TURN_CLOCKWISE[Coord.UP], Coord.RIGHT)
        self.assertEqual(Coord.TURN_CLOCKWISE[Coord.RIGHT], Coord.DOWN)
        self.assertEqual(Coord.TURN_CLOCKWISE[Coord.DOWN], Coord.LEFT)
        self.assertEqual(Coord.TURN_CLOCKWISE[Coord.LEFT], Coord.UP)

    def test_turn_counter_clockwise(self):
        """Test counter-clockwise rotation."""
        self.assertEqual(Coord.TURN_COUNTER_CLOCKWISE[Coord.UP], Coord.LEFT)
        self.assertEqual(Coord.TURN_COUNTER_CLOCKWISE[Coord.LEFT], Coord.DOWN)
        self.assertEqual(Coord.TURN_COUNTER_CLOCKWISE[Coord.DOWN], Coord.RIGHT)
        self.assertEqual(Coord.TURN_COUNTER_CLOCKWISE[Coord.RIGHT], Coord.UP)


class TestDimension(unittest.TestCase):
    """Tests for Dimension class."""

    def test_creation(self):
        """Test Dimension creation."""
        dim = Dimension(10, 5)
        self.assertEqual(dim.width, 10)
        self.assertEqual(dim.height, 5)


class TestGrid(unittest.TestCase):
    """Tests for Grid class."""

    def test_creation(self):
        """Test Grid creation."""
        data = [['A', 'B'], ['C', 'D']]
        grid = Grid(data)
        self.assertEqual(grid.size.width, 2)
        self.assertEqual(grid.size.height, 2)

    def test_create_filled(self):
        """Test Grid.create factory method."""
        grid = Grid.create(Dimension(3, 2), '.')
        self.assertEqual(grid.size.width, 3)
        self.assertEqual(grid.size.height, 2)
        self.assertEqual(grid[Coord.from_rc(0, 0)], '.')
        self.assertEqual(grid[Coord.from_rc(1, 2)], '.')

    def test_getitem(self):
        """Test grid indexing with Coord."""
        data = [['A', 'B'], ['C', 'D']]
        grid = Grid(data)

        self.assertEqual(grid[Coord.from_rc(0, 0)], 'A')
        self.assertEqual(grid[Coord.from_rc(0, 1)], 'B')
        self.assertEqual(grid[Coord.from_rc(1, 0)], 'C')
        self.assertEqual(grid[Coord.from_rc(1, 1)], 'D')

    def test_setitem(self):
        """Test grid assignment with Coord."""
        data = [['A', 'B'], ['C', 'D']]
        grid = Grid(data)

        grid[Coord.from_rc(0, 1)] = 'X'
        self.assertEqual(grid[Coord.from_rc(0, 1)], 'X')

    def test_contains(self):
        """Test bounds checking with 'in' operator."""
        grid = Grid([['A', 'B'], ['C', 'D']])

        self.assertTrue(Coord.from_rc(0, 0) in grid)
        self.assertTrue(Coord.from_rc(1, 1) in grid)
        self.assertFalse(Coord.from_rc(2, 2) in grid)
        self.assertFalse(Coord.from_rc(-1, 0) in grid)

    def test_max_bounds(self):
        """Test max_bounds property."""
        grid = Grid([['A', 'B', 'C'], ['D', 'E', 'F']])
        max_bounds = grid.max_bounds

        self.assertEqual(max_bounds.x, 2)
        self.assertEqual(max_bounds.y, 1)

    def test_coords_iterator(self):
        """Test coords iterator."""
        grid = Grid([['A', 'B'], ['C', 'D']])
        coords_values = list(grid.coords())

        self.assertEqual(len(coords_values), 4)
        # Check that we get all coordinates
        coords = [coord for coord, _ in coords_values]
        self.assertIn(Coord.from_rc(0, 0), coords)
        self.assertIn(Coord.from_rc(0, 1), coords)
        self.assertIn(Coord.from_rc(1, 0), coords)
        self.assertIn(Coord.from_rc(1, 1), coords)

    def test_find_first(self):
        """Test find_first method."""
        grid = Grid([['A', 'B', 'A'], ['C', 'D', 'E']])

        coord = grid.find_first('A')
        self.assertIsNotNone(coord)
        self.assertEqual(grid[coord], 'A')

        coord = grid.find_first('Z')
        self.assertIsNone(coord)

    def test_find_all(self):
        """Test find_all method."""
        grid = Grid([['A', 'B', 'A'], ['C', 'A', 'E']])

        coords = grid.find_all('A')
        self.assertEqual(len(coords), 3)
        for coord in coords:
            self.assertEqual(grid[coord], 'A')

        coords = grid.find_all('Z')
        self.assertEqual(len(coords), 0)

    def test_group_by_value(self):
        """Test group_by_value method."""
        grid = Grid([['A', 'B', 'A'], ['#', 'B', '#']])

        groups = grid.group_by_value()
        self.assertIn('A', groups)
        self.assertIn('B', groups)
        self.assertIn('#', groups)
        self.assertEqual(len(groups['A']), 2)
        self.assertEqual(len(groups['B']), 2)
        self.assertEqual(len(groups['#']), 2)

    def test_group_by_value_with_exclude(self):
        """Test group_by_value with exclude."""
        grid = Grid([['A', 'B', 'A'], ['#', 'B', '#']])

        groups = grid.group_by_value(exclude='#')
        self.assertIn('A', groups)
        self.assertIn('B', groups)
        self.assertNotIn('#', groups)

    def test_search_in_direction(self):
        """Test search_in_direction method."""
        grid = Grid([['X', 'M', 'A', 'S'], ['B', 'C', 'D', 'E']])

        # Search horizontally
        found = grid.search_in_direction(Coord.from_rc(0, 0), Coord.RIGHT, "XMAS")
        self.assertTrue(found)

        found = grid.search_in_direction(Coord.from_rc(0, 0), Coord.RIGHT, "XMAZ")
        self.assertFalse(found)


class TestFilterCoordsInBounds(unittest.TestCase):
    """Tests for filter_coords_in_bounds function."""

    def test_filter_basic(self):
        """Test basic coordinate filtering."""
        coords = [Coord(0, 0), Coord(5, 5), Coord(11, 11), Coord(-1, 5)]
        max_bounds = Coord(10, 10)

        filtered = filter_coords_in_bounds(coords, max_bounds)

        self.assertEqual(len(filtered), 2)
        self.assertIn(Coord(0, 0), filtered)
        self.assertIn(Coord(5, 5), filtered)
        self.assertNotIn(Coord(11, 11), filtered)
        self.assertNotIn(Coord(-1, 5), filtered)


if __name__ == '__main__':
    unittest.main()
