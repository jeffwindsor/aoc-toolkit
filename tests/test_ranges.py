"""Tests for range and interval operations."""

import unittest
from aoc.ranges import (
    merge_ranges,
    intersect_ranges,
    subtract_range,
    range_contains,
    range_overlaps,
    range_length,
    total_coverage,
)


class TestMergeRanges(unittest.TestCase):
    """Test merge_ranges function."""

    def test_merge_overlapping_ranges(self):
        """Test merging overlapping ranges."""
        self.assertEqual(merge_ranges([(1, 5), (3, 7)]), [(1, 7)])
        self.assertEqual(merge_ranges([(1, 5), (4, 8), (7, 10)]), [(1, 10)])

    def test_merge_adjacent_ranges(self):
        """Test merging adjacent ranges."""
        self.assertEqual(merge_ranges([(1, 3), (4, 6), (7, 9)]), [(1, 9)])
        self.assertEqual(merge_ranges([(1, 2), (3, 4)]), [(1, 4)])

    def test_merge_separate_ranges(self):
        """Test non-overlapping ranges remain separate."""
        self.assertEqual(merge_ranges([(1, 3), (5, 7), (10, 12)]), [(1, 3), (5, 7), (10, 12)])

    def test_merge_unsorted_ranges(self):
        """Test that unsorted ranges are handled correctly."""
        self.assertEqual(merge_ranges([(5, 10), (1, 3), (15, 20)]), [(1, 3), (5, 10), (15, 20)])

    def test_merge_empty_ranges(self):
        """Test empty input."""
        self.assertEqual(merge_ranges([]), [])

    def test_merge_single_range(self):
        """Test single range."""
        self.assertEqual(merge_ranges([(1, 5)]), [(1, 5)])

    def test_merge_duplicate_ranges(self):
        """Test duplicate ranges."""
        self.assertEqual(merge_ranges([(1, 5), (1, 5)]), [(1, 5)])

    def test_merge_nested_ranges(self):
        """Test ranges completely contained in others."""
        self.assertEqual(merge_ranges([(1, 10), (3, 5), (7, 8)]), [(1, 10)])


class TestIntersectRanges(unittest.TestCase):
    """Test intersect_ranges function."""

    def test_overlapping_ranges(self):
        """Test ranges that overlap."""
        self.assertEqual(intersect_ranges((1, 5), (3, 7)), (3, 5))
        self.assertEqual(intersect_ranges((3, 7), (1, 5)), (3, 5))

    def test_non_overlapping_ranges(self):
        """Test ranges that don't overlap."""
        self.assertIsNone(intersect_ranges((1, 3), (5, 7)))
        self.assertIsNone(intersect_ranges((5, 7), (1, 3)))

    def test_adjacent_ranges(self):
        """Test adjacent ranges (touching at boundary)."""
        self.assertEqual(intersect_ranges((1, 3), (3, 5)), (3, 3))

    def test_contained_range(self):
        """Test one range completely contained in another."""
        self.assertEqual(intersect_ranges((1, 10), (3, 5)), (3, 5))
        self.assertEqual(intersect_ranges((3, 5), (1, 10)), (3, 5))

    def test_identical_ranges(self):
        """Test identical ranges."""
        self.assertEqual(intersect_ranges((1, 5), (1, 5)), (1, 5))


class TestSubtractRange(unittest.TestCase):
    """Test subtract_range function."""

    def test_subtract_middle(self):
        """Test subtracting from middle of range."""
        self.assertEqual(subtract_range((1, 10), (5, 7)), [(1, 4), (8, 10)])

    def test_subtract_left(self):
        """Test subtracting from left side."""
        self.assertEqual(subtract_range((1, 10), (1, 5)), [(6, 10)])

    def test_subtract_right(self):
        """Test subtracting from right side."""
        self.assertEqual(subtract_range((1, 10), (5, 10)), [(1, 4)])

    def test_subtract_all(self):
        """Test subtracting entire range."""
        self.assertEqual(subtract_range((5, 7), (1, 10)), [])
        self.assertEqual(subtract_range((5, 7), (5, 7)), [])

    def test_subtract_none(self):
        """Test subtracting non-overlapping range."""
        self.assertEqual(subtract_range((1, 10), (11, 15)), [(1, 10)])
        self.assertEqual(subtract_range((5, 10), (1, 3)), [(5, 10)])


class TestRangeContains(unittest.TestCase):
    """Test range_contains function."""

    def test_contains_true(self):
        """Test cases where outer contains inner."""
        self.assertTrue(range_contains((1, 10), (3, 7)))
        self.assertTrue(range_contains((1, 10), (1, 10)))
        self.assertTrue(range_contains((5, 10), (5, 7)))

    def test_contains_false(self):
        """Test cases where outer doesn't contain inner."""
        self.assertFalse(range_contains((1, 10), (5, 15)))
        self.assertFalse(range_contains((5, 10), (1, 7)))
        self.assertFalse(range_contains((1, 5), (6, 10)))


class TestRangeOverlaps(unittest.TestCase):
    """Test range_overlaps function."""

    def test_overlaps_true(self):
        """Test cases where ranges overlap."""
        self.assertTrue(range_overlaps((1, 5), (3, 7)))
        self.assertTrue(range_overlaps((1, 5), (5, 7)))
        self.assertTrue(range_overlaps((3, 7), (1, 5)))

    def test_overlaps_false(self):
        """Test cases where ranges don't overlap."""
        self.assertFalse(range_overlaps((1, 3), (5, 7)))
        self.assertFalse(range_overlaps((5, 7), (1, 3)))

    def test_overlaps_contained(self):
        """Test contained ranges overlap."""
        self.assertTrue(range_overlaps((1, 10), (3, 5)))


class TestRangeLength(unittest.TestCase):
    """Test range_length function."""

    def test_various_lengths(self):
        """Test calculating range lengths."""
        self.assertEqual(range_length((1, 5)), 5)
        self.assertEqual(range_length((0, 99)), 100)
        self.assertEqual(range_length((10, 10)), 1)
        self.assertEqual(range_length((5, 14)), 10)


class TestTotalCoverage(unittest.TestCase):
    """Test total_coverage function."""

    def test_overlapping_coverage(self):
        """Test coverage with overlapping ranges."""
        self.assertEqual(total_coverage([(1, 5), (3, 7)]), 7)

    def test_separate_coverage(self):
        """Test coverage with separate ranges."""
        self.assertEqual(total_coverage([(1, 3), (5, 7), (10, 12)]), 9)

    def test_nested_coverage(self):
        """Test coverage with nested ranges."""
        self.assertEqual(total_coverage([(1, 10), (3, 5)]), 10)

    def test_empty_coverage(self):
        """Test empty ranges."""
        self.assertEqual(total_coverage([]), 0)

    def test_single_range_coverage(self):
        """Test single range."""
        self.assertEqual(total_coverage([(1, 10)]), 10)


if __name__ == '__main__':
    unittest.main()
