"""Tests for coord module."""

import unittest
from aoc import Coord


class TestCoord(unittest.TestCase):
    """Test Coord class functionality."""

    def test_creation(self):
        """Test basic coordinate creation."""
        coord = Coord(1, 2)
        self.assertEqual(coord.row, 1)
        self.assertEqual(coord.col, 2)

    def test_addition(self):
        """Test coordinate addition."""
        c1 = Coord(1, 2)
        c2 = Coord(3, 4)
        result = c1 + c2
        self.assertEqual(result, Coord(4, 6))

    def test_subtraction(self):
        """Test coordinate subtraction."""
        c1 = Coord(5, 7)
        c2 = Coord(2, 3)
        result = c1 - c2
        self.assertEqual(result, Coord(3, 4))

    def test_direction_constants(self):
        """Test direction constants exist and are correct."""
        self.assertEqual(Coord.UP, Coord(-1, 0))
        self.assertEqual(Coord.DOWN, Coord(1, 0))
        self.assertEqual(Coord.LEFT, Coord(0, -1))
        self.assertEqual(Coord.RIGHT, Coord(0, 1))

    def test_cardinal_directions(self):
        """Test cardinal direction collection."""
        self.assertEqual(len(Coord.DIRECTIONS_CARDINAL), 4)
        self.assertIn(Coord.UP, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.DOWN, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.LEFT, Coord.DIRECTIONS_CARDINAL)
        self.assertIn(Coord.RIGHT, Coord.DIRECTIONS_CARDINAL)

    def test_all_directions(self):
        """Test all directions collection includes diagonals."""
        self.assertEqual(len(Coord.DIRECTIONS_ALL), 8)
        self.assertIn(Coord.UP_LEFT, Coord.DIRECTIONS_ALL)
        self.assertIn(Coord.DOWN_RIGHT, Coord.DIRECTIONS_ALL)

    def test_in_bounds(self):
        """Test bounds checking."""
        coord = Coord(5, 5)
        self.assertTrue(coord.in_bounds(Coord(10, 10)))
        self.assertFalse(coord.in_bounds(Coord(3, 3)))
        self.assertTrue(coord.in_bounds(Coord(5, 5)))

    def test_manhattan_distance(self):
        """Test Manhattan distance calculation."""
        c1 = Coord(0, 0)
        c2 = Coord(3, 4)
        self.assertEqual(c1.manhattan_distance(c2), 7)

    def test_immutability(self):
        """Test that Coord is immutable (frozen)."""
        coord = Coord(1, 2)
        with self.assertRaises(AttributeError):
            coord.row = 5

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


if __name__ == "__main__":
    unittest.main()
