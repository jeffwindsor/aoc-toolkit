"""Nox sessions for testing and automation."""

import nox

# Python versions to test
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

# Default sessions when running `nox` without arguments
nox.options.sessions = ["tests"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run tests with unittest across all Python versions."""
    session.install("-e", ".")
    session.run(
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_*.py",
        "-v",
    )


@nox.session
def pytest(session):
    """Run tests with pytest (faster iteration during development)."""
    session.install("-e", ".[dev]")
    session.run("pytest")


@nox.session
def coverage(session):
    """Run tests with coverage reporting."""
    session.install("-e", ".[dev]")
    session.run("pytest", "--cov-report=term", "--cov-report=html")
    session.log("Coverage report generated in htmlcov/index.html")


@nox.session
def validate_imports(session):
    """Validate all three import styles work correctly."""
    session.install("-e", ".")

    # Test flat imports
    session.run(
        "python",
        "-c",
        "from aoc import Coord, bfs, run, TestCase; print('✓ Flat imports work')",
    )

    # Test explicit module imports
    session.run(
        "python",
        "-c",
        "from aoc.coord import Coord; from aoc.graph import bfs; print('✓ Explicit module imports work')",
    )

    # Test namespace imports
    session.run(
        "python",
        "-c",
        "import aoc; import aoc.coord; import aoc.graph; print('✓ Namespace imports work')",
    )

    session.log("✓ All import styles validated successfully")


@nox.session
def validate_all(session):
    """Run full validation: imports + tests."""
    session.install("-e", ".")

    # Validate imports
    session.log("Validating import styles...")
    session.run(
        "python", "-c", "from aoc import Coord, bfs, run, TestCase"
    )
    session.run(
        "python", "-c", "from aoc.coord import Coord; from aoc.graph import bfs"
    )
    session.run(
        "python", "-c", "import aoc; import aoc.coord; import aoc.graph"
    )
    session.log("✓ Import validation passed")

    # Run tests
    session.log("\nRunning tests...")
    session.run(
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_*.py",
        "-v",
    )
