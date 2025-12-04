"""Testing utilities for Advent of Code puzzles."""

import os
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Any


# ========== Configuration ==========
def _is_perf_enabled() -> bool:
    config_file = ".aoc_config"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("test_performance_tracking="):
                        value = line.split("=", 1)[1].strip().lower()
                        return value in ("true", "1", "yes")
        except Exception:
            pass
    return False


# Cache at module load time for zero per-test overhead
PERF_ENABLED = _is_perf_enabled()


# ========== Colors ==========

TITLE_COLOR = "\033[1m\033[34m"  # Bold blue
FALSE_COLOR = "\033[91m"          # Bright red
TRUE_COLOR = "\033[92m"           # Bright green
GRAY_COLOR = "\033[90m"           # Dim gray
YELLOW_COLOR = "\033[93m"         # Bright yellow
END_COLOR = "\033[0m"

# Symbols
PASS_SYMBOL = "✓"
FAIL_SYMBOL = "✗"


# ========== Formatting ==========


def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f} µs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def format_memory(bytes_used: int) -> str:
    if bytes_used < 1024:
        return f"{bytes_used} B"
    elif bytes_used < 1024 * 1024:
        return f"{bytes_used / 1024:.1f} KB"
    else:
        return f"{bytes_used / (1024 * 1024):.1f} MB"


# ========== Test Framework ==========


@dataclass
class TestCase:
    data_file: str
    expected: Any = None


def _load_answer_file(data_file: str, part: str) -> Any | None:
    """
    Load expected answer from .{part}.answer file if it exists.

    Args:
        data_file: Name of the data file (e.g., "04_example_01")
        part: Part identifier (e.g., "part1", "part2")

    Returns:
        Parsed answer value or None if file doesn't exist
    """
    answer_path = f"data/{data_file}.{part}.answer"

    if os.path.exists(answer_path):
        try:
            with open(answer_path, "r") as f:
                content = f.read().strip()
                # Try to parse as int first, then float, then keep as string
                try:
                    return int(content)
                except ValueError:
                    try:
                        return float(content)
                    except ValueError:
                        return content
        except Exception:
            pass
    return None


@dataclass
class _TestResult:
    """Internal class to store test failure details."""

    test_case: TestCase
    expected: Any
    actual: Any
    error: Exception | None
    elapsed_time: float
    peak_mem: int


def run(func: Callable[[str], Any], test_cases: list[TestCase], part: str) -> None:
    """
    Execute test cases for a given function and report results with performance metrics.

    If TestCase.expected is None, attempts to load from data/{data_file}.{part}.answer

    Args:
        func: Function to test
        test_cases: List of test cases
        part: Part identifier (required: "part1" or "part2")
    """

    print(f"{TITLE_COLOR}{func.__name__}{END_COLOR}")

    passed = 0
    failed = 0
    failures: list[_TestResult] = []
    total_time = 0.0

    for test_case in test_cases:
        # Load expected value from answer file if not provided
        expected = test_case.expected
        if expected is None:
            expected = _load_answer_file(test_case.data_file, part)

        elapsed_time = 0.0
        peak_mem = 0
        actual = None
        error = None

        try:
            # Start performance tracking (if enabled)
            if PERF_ENABLED:
                tracemalloc.start()
                start_time = time.perf_counter()

            # Execute test
            actual = func(test_case.data_file)

            # Capture metrics (if enabled)
            if PERF_ENABLED:
                elapsed_time = time.perf_counter() - start_time
                _, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                total_time += elapsed_time

        except Exception as e:
            # Stop tracking on error (if enabled)
            if PERF_ENABLED:
                if tracemalloc.is_tracing():
                    elapsed_time = time.perf_counter() - start_time
                    _, peak_mem = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                total_time += elapsed_time
            error = e

        # Determine pass/fail
        if error is not None:
            # Exception occurred
            symbol = FAIL_SYMBOL
            color = FALSE_COLOR
            status = "ERROR"
            failures.append(
                _TestResult(test_case, expected, actual, error, elapsed_time, peak_mem)
            )
            failed += 1
        elif expected is None:
            # No expected value
            symbol = FAIL_SYMBOL
            color = FALSE_COLOR
            status = "NO EXPECTED"
            failures.append(
                _TestResult(test_case, expected, actual, None, elapsed_time, peak_mem)
            )
            failed += 1
        elif expected == actual:
            # Test passed
            symbol = PASS_SYMBOL
            color = TRUE_COLOR
            status = str(actual)
            passed += 1
        else:
            # Wrong answer
            symbol = FAIL_SYMBOL
            color = FALSE_COLOR
            status = f"expected {expected}, got {actual}"
            failures.append(
                _TestResult(test_case, expected, actual, None, elapsed_time, peak_mem)
            )
            failed += 1

        # Format metrics
        if PERF_ENABLED:
            time_str = format_time(elapsed_time)
            mem_str = format_memory(peak_mem)
            metrics = f"{GRAY_COLOR}({time_str}, {mem_str}){END_COLOR}"
        else:
            metrics = ""

        # Print inline result
        print(f"  {color}{symbol}{END_COLOR} {test_case.data_file}: {color}{status}{END_COLOR} {metrics}")

    # Print detailed failure section (pytest-style)
    if failures:
        print(f"\n{FALSE_COLOR}{'=' * 70}{END_COLOR}")
        print(f"{FALSE_COLOR}FAILURES{END_COLOR}")
        print(f"{FALSE_COLOR}{'=' * 70}{END_COLOR}")

        for result in failures:
            print(f"\n{YELLOW_COLOR}{result.test_case.data_file}{END_COLOR}")

            if result.error is not None:
                # Exception case
                print(f"  {FALSE_COLOR}ERROR: {type(result.error).__name__}: {result.error}{END_COLOR}")
            elif result.expected is None:
                # No expected value
                print(f"  {FALSE_COLOR}No expected value{END_COLOR}")
                print(f"  {GRAY_COLOR}(missing .{part}.answer file or TestCase.expected parameter){END_COLOR}")
                print(f"  Actual: {result.actual}")
            else:
                # Wrong answer
                print(f"  Expected: {result.expected}")
                print(f"  Actual:   {FALSE_COLOR}{result.actual}{END_COLOR}")

            if PERF_ENABLED:
                time_str = format_time(result.elapsed_time)
                mem_str = format_memory(result.peak_mem)
                print(f"  {GRAY_COLOR}({time_str}, {mem_str}){END_COLOR}")

        print(f"{FALSE_COLOR}{'=' * 70}{END_COLOR}")

    # Print summary (pytest-style)
    total = passed + failed
    summary_parts = []

    if passed > 0:
        summary_parts.append(f"{TRUE_COLOR}{passed} passed{END_COLOR}")
    if failed > 0:
        summary_parts.append(f"{FALSE_COLOR}{failed} failed{END_COLOR}")

    summary = ", ".join(summary_parts)

    if PERF_ENABLED:
        time_str = format_time(total_time)
        print(f"\n{summary} in {time_str}")
    else:
        print(f"\n{summary}")

    print()


__all__ = [
    "TestCase",
    "run",
    "PERF_ENABLED",
    "format_time",
    "format_memory",
]
