"""Tests for range and interval operations."""

import pytest
from aoc.ranges import (
    merge_ranges,
    intersect_ranges,
    subtract_range,
    range_contains,
    range_overlaps,
    range_length,
    total_coverage,
)


class TestMergeRanges:
    """Test merge_ranges function."""

    def test_merge_overlapping_ranges(self):
        """Test merging overlapping ranges."""
        assert merge_ranges([(1, 5), (3, 7)]) == [(1, 7)]
        assert merge_ranges([(1, 5), (4, 8), (7, 10)]) == [(1, 10)]

    def test_merge_adjacent_ranges(self):
        """Test merging adjacent ranges."""
        assert merge_ranges([(1, 3), (4, 6), (7, 9)]) == [(1, 9)]
        assert merge_ranges([(1, 2), (3, 4)]) == [(1, 4)]

    def test_merge_separate_ranges(self):
        """Test non-overlapping ranges remain separate."""
        assert merge_ranges([(1, 3), (5, 7), (10, 12)]) == [(1, 3), (5, 7), (10, 12)]

    def test_merge_unsorted_ranges(self):
        """Test that unsorted ranges are handled correctly."""
        assert merge_ranges([(5, 10), (1, 3), (15, 20)]) == [(1, 3), (5, 10), (15, 20)]

    def test_merge_empty_ranges(self):
        """Test empty input."""
        assert merge_ranges([]) == []

    def test_merge_single_range(self):
        """Test single range."""
        assert merge_ranges([(1, 5)]) == [(1, 5)]

    def test_merge_duplicate_ranges(self):
        """Test duplicate ranges."""
        assert merge_ranges([(1, 5), (1, 5)]) == [(1, 5)]

    def test_merge_nested_ranges(self):
        """Test ranges completely contained in others."""
        assert merge_ranges([(1, 10), (3, 5), (7, 8)]) == [(1, 10)]


class TestIntersectRanges:
    """Test intersect_ranges function."""

    def test_overlapping_ranges(self):
        """Test ranges that overlap."""
        assert intersect_ranges((1, 5), (3, 7)) == (3, 5)
        assert intersect_ranges((3, 7), (1, 5)) == (3, 5)

    def test_non_overlapping_ranges(self):
        """Test ranges that don't overlap."""
        assert intersect_ranges((1, 3), (5, 7)) is None
        assert intersect_ranges((5, 7), (1, 3)) is None

    def test_adjacent_ranges(self):
        """Test adjacent ranges (touching at boundary)."""
        assert intersect_ranges((1, 3), (3, 5)) == (3, 3)

    def test_contained_range(self):
        """Test one range completely contained in another."""
        assert intersect_ranges((1, 10), (3, 5)) == (3, 5)
        assert intersect_ranges((3, 5), (1, 10)) == (3, 5)

    def test_identical_ranges(self):
        """Test identical ranges."""
        assert intersect_ranges((1, 5), (1, 5)) == (1, 5)


class TestSubtractRange:
    """Test subtract_range function."""

    def test_subtract_middle(self):
        """Test subtracting from middle of range."""
        assert subtract_range((1, 10), (5, 7)) == [(1, 4), (8, 10)]

    def test_subtract_left(self):
        """Test subtracting from left side."""
        assert subtract_range((1, 10), (1, 5)) == [(6, 10)]

    def test_subtract_right(self):
        """Test subtracting from right side."""
        assert subtract_range((1, 10), (5, 10)) == [(1, 4)]

    def test_subtract_all(self):
        """Test subtracting entire range."""
        assert subtract_range((5, 7), (1, 10)) == []
        assert subtract_range((5, 7), (5, 7)) == []

    def test_subtract_none(self):
        """Test subtracting non-overlapping range."""
        assert subtract_range((1, 10), (11, 15)) == [(1, 10)]
        assert subtract_range((5, 10), (1, 3)) == [(5, 10)]


class TestRangeContains:
    """Test range_contains function."""

    def test_contains_true(self):
        """Test cases where outer contains inner."""
        assert range_contains((1, 10), (3, 7)) is True
        assert range_contains((1, 10), (1, 10)) is True
        assert range_contains((5, 10), (5, 7)) is True

    def test_contains_false(self):
        """Test cases where outer doesn't contain inner."""
        assert range_contains((1, 10), (5, 15)) is False
        assert range_contains((5, 10), (1, 7)) is False
        assert range_contains((1, 5), (6, 10)) is False


class TestRangeOverlaps:
    """Test range_overlaps function."""

    def test_overlaps_true(self):
        """Test cases where ranges overlap."""
        assert range_overlaps((1, 5), (3, 7)) is True
        assert range_overlaps((1, 5), (5, 7)) is True
        assert range_overlaps((3, 7), (1, 5)) is True

    def test_overlaps_false(self):
        """Test cases where ranges don't overlap."""
        assert range_overlaps((1, 3), (5, 7)) is False
        assert range_overlaps((5, 7), (1, 3)) is False

    def test_overlaps_contained(self):
        """Test contained ranges overlap."""
        assert range_overlaps((1, 10), (3, 5)) is True


class TestRangeLength:
    """Test range_length function."""

    def test_various_lengths(self):
        """Test calculating range lengths."""
        assert range_length((1, 5)) == 5
        assert range_length((0, 99)) == 100
        assert range_length((10, 10)) == 1
        assert range_length((5, 14)) == 10


class TestTotalCoverage:
    """Test total_coverage function."""

    def test_overlapping_coverage(self):
        """Test coverage with overlapping ranges."""
        assert total_coverage([(1, 5), (3, 7)]) == 7

    def test_separate_coverage(self):
        """Test coverage with separate ranges."""
        assert total_coverage([(1, 3), (5, 7), (10, 12)]) == 9

    def test_nested_coverage(self):
        """Test coverage with nested ranges."""
        assert total_coverage([(1, 10), (3, 5)]) == 10

    def test_empty_coverage(self):
        """Test empty ranges."""
        assert total_coverage([]) == 0

    def test_single_range_coverage(self):
        """Test single range."""
        assert total_coverage([(1, 10)]) == 10
