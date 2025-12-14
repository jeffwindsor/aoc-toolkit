"""Tests for graph algorithms."""

import unittest
from aoc.graph import (
    bfs, dfs, dijkstra, bfs_grid_path, dfs_grid_path,
    flood_fill, flood_fill_mark, count_paths_dag, count_paths_cyclic,
    find_max_clique, UnionFind
)
from aoc.d2 import Coord, Grid


class TestBFS(unittest.TestCase):
    """Tests for breadth-first search."""

    def test_bfs_distances(self):
        """Test BFS distance calculation."""
        # Simple graph: 0 -> 1 -> 2 -> 3
        def neighbors(node):
            if node == 0:
                return [1]
            elif node == 1:
                return [0, 2]
            elif node == 2:
                return [1, 3]
            elif node == 3:
                return [2]
            return []

        distances = bfs(0, neighbors)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[2], 2)
        self.assertEqual(distances[3], 3)

    def test_bfs_path(self):
        """Test BFS pathfinding."""
        def neighbors(node):
            graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}
            return graph.get(node, [])

        def goal(node):
            return node == 4

        path = bfs(0, neighbors, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 4)
        self.assertEqual(len(path), 4)  # Shortest path: 0 -> (1 or 2) -> 3 -> 4


class TestDFS(unittest.TestCase):
    """Tests for depth-first search."""

    def test_dfs_path(self):
        """Test DFS pathfinding."""
        def neighbors(node):
            graph = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}
            return graph.get(node, [])

        def goal(node):
            return node == 4

        path = dfs(0, neighbors, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 4)

    def test_dfs_no_path(self):
        """Test DFS when no path exists."""
        def neighbors(node):
            return []

        def goal(node):
            return node == 10

        path = dfs(0, neighbors, goal)
        self.assertIsNone(path)


class TestDijkstra(unittest.TestCase):
    """Tests for Dijkstra's algorithm."""

    def test_dijkstra_weighted(self):
        """Test Dijkstra with weighted edges."""
        def neighbors(node):
            graph = {
                0: [(1, 1), (2, 4)],
                1: [(2, 2), (3, 5)],
                2: [(3, 1)],
                3: []
            }
            return graph.get(node, [])

        distances = dijkstra(0, neighbors)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[2], 3)
        self.assertEqual(distances[3], 4)

    def test_dijkstra_with_goal(self):
        """Test Dijkstra with early termination."""
        def neighbors(node):
            graph = {
                0: [(1, 1), (2, 4)],
                1: [(2, 2), (3, 5)],
                2: [(3, 1)],
                3: []
            }
            return graph.get(node, [])

        distances = dijkstra(0, neighbors, goal=3)
        self.assertEqual(distances[3], 4)


class TestGridPathfinding(unittest.TestCase):
    """Tests for grid pathfinding functions."""

    def test_bfs_grid_path(self):
        """Test BFS grid pathfinding."""
        grid = Grid([
            ['.', '.', '#', '.'],
            ['.', '#', '#', '.'],
            ['.', '.', '.', '.']
        ])

        start = Coord.from_rc(0, 0)
        end = Coord.from_rc(2, 3)
        path = bfs_grid_path(grid, start, end, {'.'}  )

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)

    def test_bfs_grid_path_blocked(self):
        """Test BFS grid pathfinding with blocked path."""
        grid = Grid([
            ['.', '.', '#'],
            ['#', '#', '#'],
            ['.', '.', '.']
        ])

        start = Coord.from_rc(0, 0)
        end = Coord.from_rc(2, 2)
        path = bfs_grid_path(grid, start, end, {'.'})

        self.assertIsNone(path)

    def test_dfs_grid_path(self):
        """Test DFS grid pathfinding."""
        grid = Grid([
            ['.', '.', '.'],
            ['.', '#', '.'],
            ['.', '.', '.']
        ])

        start = Coord.from_rc(0, 0)
        end = Coord.from_rc(2, 2)
        path = dfs_grid_path(grid, start, end, {'.'})

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)


class TestFloodFill(unittest.TestCase):
    """Tests for flood fill algorithms."""

    def test_flood_fill_basic(self):
        """Test basic flood fill."""
        grid = Grid([
            ['.', '.', '#', '.'],
            ['.', '#', '#', '.'],
            ['.', '.', '.', '#']
        ])

        start = Coord.from_rc(0, 0)
        region = flood_fill(grid, start, {'.'})

        # Should fill connected region
        self.assertIn(Coord.from_rc(0, 0), region)
        self.assertIn(Coord.from_rc(0, 1), region)
        self.assertIn(Coord.from_rc(1, 0), region)
        self.assertNotIn(Coord.from_rc(0, 3), region)  # Blocked by wall

    def test_flood_fill_mark(self):
        """Test destructive flood fill marking."""
        grid = Grid([
            ['.', '.', '#'],
            ['.', '#', '.'],
            ['.', '.', '.']
        ])

        start = Coord.from_rc(0, 0)
        flood_fill_mark(grid, start, 'X', {'.'})

        # Check marked cells
        self.assertEqual(grid[Coord.from_rc(0, 0)], 'X')
        self.assertEqual(grid[Coord.from_rc(0, 1)], 'X')
        self.assertEqual(grid[Coord.from_rc(1, 0)], 'X')
        # Blocked by wall
        self.assertEqual(grid[Coord.from_rc(0, 2)], '#')
        # Can reach (2,2) via (2,0) -> (2,1) -> (2,2)
        self.assertEqual(grid[Coord.from_rc(2, 2)], 'X')


class TestPathCounting(unittest.TestCase):
    """Tests for path counting algorithms."""

    def test_count_paths_dag(self):
        """Test path counting in DAG."""
        def neighbors(node):
            graph = {
                0: [1, 2],
                1: [3],
                2: [3],
                3: [4],
                4: []
            }
            return graph.get(node, [])

        def goal(node):
            return node == 4

        count = count_paths_dag(0, neighbors, goal)
        self.assertEqual(count, 2)  # 0->1->3->4 and 0->2->3->4

    def test_count_paths_cyclic(self):
        """Test path counting in cyclic graph."""
        def neighbors(node):
            graph = {
                0: [1],
                1: [2],
                2: [3, 0],  # Cycle back to 0
                3: []
            }
            return graph.get(node, [])

        def goal(node):
            return node == 3

        count = count_paths_cyclic(0, neighbors, goal)
        self.assertEqual(count, 1)  # Only 0->1->2->3 (doesn't follow cycle)


class TestMaxClique(unittest.TestCase):
    """Tests for maximum clique finding."""

    def test_find_max_clique_triangle(self):
        """Test finding max clique in triangle."""
        graph = {
            'A': {'B', 'C'},
            'B': {'A', 'C'},
            'C': {'A', 'B'}
        }

        clique = find_max_clique(graph)
        self.assertEqual(len(clique), 3)
        self.assertEqual(clique, {'A', 'B', 'C'})

    def test_find_max_clique_complex(self):
        """Test finding max clique in complex graph."""
        graph = {
            'A': {'B', 'C', 'D'},
            'B': {'A', 'C'},
            'C': {'A', 'B', 'D'},
            'D': {'A', 'C', 'E'},
            'E': {'D'}
        }

        clique = find_max_clique(graph)
        # Max clique should be {A, C, D} or similar
        self.assertGreaterEqual(len(clique), 3)


class TestUnionFind(unittest.TestCase):
    """Tests for UnionFind data structure."""

    def test_union_find_basic(self):
        """Test basic union and find operations."""
        uf = UnionFind()

        uf.union('A', 'B')
        uf.union('C', 'D')

        self.assertEqual(uf.find('A'), uf.find('B'))
        self.assertNotEqual(uf.find('A'), uf.find('C'))

    def test_union_find_transitive(self):
        """Test transitive union."""
        uf = UnionFind()

        uf.union('A', 'B')
        uf.union('B', 'C')

        # A, B, C should all be in same component
        self.assertEqual(uf.find('A'), uf.find('C'))

    def test_get_component_sizes(self):
        """Test getting component sizes."""
        uf = UnionFind()

        uf.union('A', 'B')
        uf.union('B', 'C')
        uf.union('D', 'E')

        sizes = uf.get_component_sizes()
        self.assertIn(3, sizes.values())  # Component {A, B, C}
        self.assertIn(2, sizes.values())  # Component {D, E}

    def test_count_components(self):
        """Test counting components."""
        uf = UnionFind()

        uf.union('A', 'B')
        uf.union('C', 'D')
        uf.union('E', 'F')

        self.assertEqual(uf.count_components(), 3)

        uf.union('A', 'C')
        self.assertEqual(uf.count_components(), 2)

    def test_single_element(self):
        """Test single element component."""
        uf = UnionFind()

        # Just accessing an element creates a component
        root = uf.find('A')
        self.assertIsNotNone(root)
        self.assertEqual(uf.count_components(), 1)


if __name__ == '__main__':
    unittest.main()
