"""Tests for math module."""

import unittest
from aoc import count_continuous_segments, count_digits


class TestMath(unittest.TestCase):
    """Test math utilities."""

    def test_count_continuous_segments(self):
        """Test counting continuous segments."""
        # Single segment
        self.assertEqual(count_continuous_segments([1, 2, 3, 4]), 1)

        # Two segments
        self.assertEqual(count_continuous_segments([1, 2, 5, 6]), 2)

        # Three segments
        self.assertEqual(count_continuous_segments([0, 1, 2, 5, 6, 10]), 3)

        # All separate
        self.assertEqual(count_continuous_segments([1, 3, 5, 7]), 4)

        # Empty list
        self.assertEqual(count_continuous_segments([]), 0)

        # Single element
        self.assertEqual(count_continuous_segments([5]), 1)

    def test_count_digits(self):
        """Test digit counting."""
        self.assertEqual(count_digits(0), 1)
        self.assertEqual(count_digits(5), 1)
        self.assertEqual(count_digits(123), 3)
        self.assertEqual(count_digits(9999), 4)
        self.assertEqual(count_digits(1000000), 7)


if __name__ == "__main__":
    unittest.main()
