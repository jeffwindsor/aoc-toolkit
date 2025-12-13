"""Number and math utility functions."""


def count_continuous_segments(sorted_coords: list[int]) -> int:
    """
    Count continuous segments in sorted coordinates.

    Args:
        sorted_coords: List of sorted integers

    Returns:
        Number of continuous segments

    Examples:
        >>> count_continuous_segments([0, 1, 2, 5, 6])
        2  # Two segments: [0,1,2] and [5,6]
        >>> count_continuous_segments([0, 1, 2])
        1  # One segment
        >>> count_continuous_segments([0, 2, 4])
        3  # Three segments
    """
    if not sorted_coords:
        return 0

    segments = 1
    for i in range(1, len(sorted_coords)):
        if sorted_coords[i] != sorted_coords[i - 1] + 1:
            segments += 1
    return segments


def count_digits(n: int) -> int:
    """
    Count the number of digits in a positive integer.

    Args:
        n: A non-negative integer

    Returns:
        The number of digits in n (e.g., 123 -> 3, 0 -> 1)

    Examples:
        >>> count_digits(0)
        1
        >>> count_digits(123)
        3
        >>> count_digits(9999)
        4
    """
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


def calculate_toggle_states(toggles: list[int], size: int) -> list[bool]:
    """
    Calculate final states after multiple toggles.

    Each element in toggles represents an index to toggle. An element
    is ON if toggled an odd number of times (parity-based).

    Args:
        toggles: List of indices that were toggled
        size: Total number of elements

    Returns:
        List of final boolean states (True = ON)

    Examples:
        >>> calculate_toggle_states([0, 1, 0, 2], 3)
        [False, True, True]
        >>> calculate_toggle_states([1, 3, 2, 3], 5)
        [False, True, True, False, False]
    """
    from collections import Counter
    counts = Counter(toggles)
    return [counts.get(i, 0) % 2 == 1 for i in range(size)]


__all__ = [
    "count_continuous_segments",
    "count_digits",
    "calculate_toggle_states",
]
