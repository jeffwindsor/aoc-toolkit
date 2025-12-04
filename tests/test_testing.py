"""Tests for testing module."""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from aoc import TestCase, run


class TestTestCase(unittest.TestCase):
    """Test TestCase dataclass."""

    def test_creation_with_expected(self):
        """Test TestCase creation with explicit expected value."""
        tc = TestCase("test_file", expected=42)
        self.assertEqual(tc.data_file, "test_file")
        self.assertEqual(tc.expected, 42)

    def test_creation_without_expected(self):
        """Test TestCase creation without expected value."""
        tc = TestCase("test_file")
        self.assertEqual(tc.data_file, "test_file")
        self.assertIsNone(tc.expected)


class TestAnswerFileLoading(unittest.TestCase):
    """Test answer file loading functionality."""

    def setUp(self):
        """Create temporary directory for test data files."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, "data")
        os.makedirs(self.data_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_int_answer(self):
        """Test loading integer answer from file."""
        answer_file = os.path.join(self.data_dir, "test.part1.answer")
        with open(answer_file, "w") as f:
            f.write("42\n")

        # Create dummy data file
        data_file = os.path.join(self.data_dir, "test")
        with open(data_file, "w") as f:
            f.write("test data\n")

        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test")], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("42", output)
            self.assertIn("1 passed", output)

    def test_load_string_answer(self):
        """Test loading string answer from file."""
        answer_file = os.path.join(self.data_dir, "test.part1.answer")
        with open(answer_file, "w") as f:
            f.write("hello\n")

        data_file = os.path.join(self.data_dir, "test")
        with open(data_file, "w") as f:
            f.write("test data\n")

        def test_func(data_file):
            return "hello"

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test")], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("hello", output)
            self.assertIn("1 passed", output)

    def test_missing_answer_file(self):
        """Test that missing answer file causes test failure."""
        data_file = os.path.join(self.data_dir, "test")
        with open(data_file, "w") as f:
            f.write("test data\n")

        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test")], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("NO EXPECTED", output)
            self.assertIn("Actual: 42", output)
            self.assertIn("1 failed", output)


class TestRunFunction(unittest.TestCase):
    """Test run() function behavior."""

    def setUp(self):
        """Create temporary directory for test data files."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, "data")
        os.makedirs(self.data_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create dummy data file
        self.data_file = os.path.join(self.data_dir, "test")
        with open(self.data_file, "w") as f:
            f.write("test data\n")

    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_pass_with_explicit_expected(self):
        """Test that test passes when actual == expected (explicit)."""
        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test", expected=42)], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("42", output)
            self.assertIn("1 passed", output)
            self.assertNotIn("failed", output)

    def test_fail_with_wrong_expected(self):
        """Test that test fails when actual != expected."""
        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test", expected=100)], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("expected 100, got 42", output)
            self.assertIn("1 failed", output)

    def test_fail_without_expected_value(self):
        """Test that test fails when no expected value provided (critical bug fix)."""
        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test")], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("NO EXPECTED", output)
            self.assertIn("Actual: 42", output)
            self.assertIn("1 failed", output)

    def test_multiple_tests_mixed_results(self):
        """Test multiple test cases with mixed pass/fail results."""
        def test_func(data_file):
            if "pass" in data_file:
                return 42
            else:
                return 100

        # Create pass and fail data files
        pass_file = os.path.join(self.data_dir, "test_pass")
        fail_file = os.path.join(self.data_dir, "test_fail")
        with open(pass_file, "w") as f:
            f.write("pass data\n")
        with open(fail_file, "w") as f:
            f.write("fail data\n")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(
                test_func,
                [
                    TestCase("test_pass", expected=42),
                    TestCase("test_fail", expected=42),
                ],
                part="part1",
            )
            output = mock_stdout.getvalue()
            self.assertIn("1 passed", output)
            self.assertIn("1 failed", output)

    def test_exception_handling(self):
        """Test that exceptions are caught and reported."""
        def test_func(data_file):
            raise ValueError("Test error")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run(test_func, [TestCase("test", expected=42)], part="part1")
            output = mock_stdout.getvalue()
            self.assertIn("ERROR: ValueError: Test error", output)
            self.assertIn("1 failed", output)


class TestPerformanceTracking(unittest.TestCase):
    """Test performance tracking functionality."""

    def setUp(self):
        """Create temporary directory for test config."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create data directory and file
        os.makedirs("data")
        with open("data/test", "w") as f:
            f.write("test data\n")

    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_performance_tracking_enabled(self):
        """Test that performance metrics appear when enabled."""
        # Create config file with performance tracking enabled
        with open(".aoc_config", "w") as f:
            f.write("test_performance_tracking=true\n")

        # Reload module to pick up config
        import aoc.testing
        import importlib
        importlib.reload(aoc.testing)

        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            from aoc.testing import run
            run(test_func, [TestCase("test", expected=42)], part="part1")
            output = mock_stdout.getvalue()
            # Should contain time and memory metrics
            self.assertTrue("µs" in output or "ms" in output or "s" in output)
            self.assertTrue("KB" in output or "MB" in output or "B" in output)

    def test_performance_tracking_disabled(self):
        """Test that performance metrics don't appear when disabled."""
        # No config file = disabled
        if os.path.exists(".aoc_config"):
            os.remove(".aoc_config")

        # Reload module to pick up config
        import aoc.testing
        import importlib
        importlib.reload(aoc.testing)

        def test_func(data_file):
            return 42

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            from aoc.testing import run
            run(test_func, [TestCase("test", expected=42)], part="part1")
            output = mock_stdout.getvalue()
            # Should NOT contain time and memory metrics
            self.assertNotIn("µs", output)
            self.assertNotIn("ms", output)
            self.assertNotIn("KB", output)
            self.assertNotIn("MB", output)


if __name__ == "__main__":
    unittest.main()
