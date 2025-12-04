"""Tests for graph module."""

import unittest
from aoc import bfs, dfs, dijkstra, find_max_clique


class TestGraph(unittest.TestCase):
    """Test graph algorithms."""

    def test_bfs_distances(self):
        """Test BFS distance calculation."""
        def neighbors(node):
            graph = {
                'A': ['B', 'C'],
                'B': ['D'],
                'C': ['D'],
                'D': []
            }
            return graph.get(node, [])

        distances = bfs('A', neighbors)
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 1)
        self.assertEqual(distances['C'], 1)
        self.assertEqual(distances['D'], 2)

    def test_bfs_path_to_goal(self):
        """Test BFS path finding."""
        def neighbors(node):
            graph = {
                'A': ['B', 'C'],
                'B': ['D'],
                'C': ['D'],
                'D': []
            }
            return graph.get(node, [])

        def goal(node):
            return node == 'D'

        path = bfs('A', neighbors, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
        self.assertTrue(len(path) in [3])  # Either A->B->D or A->C->D

    def test_dfs_path(self):
        """Test DFS path finding."""
        def neighbors(node):
            graph = {
                'A': ['B', 'C'],
                'B': ['D'],
                'C': ['D'],
                'D': []
            }
            return graph.get(node, [])

        def goal(node):
            return node == 'D'

        path = dfs('A', neighbors, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')

    def test_dijkstra_distances(self):
        """Test Dijkstra with weighted edges."""
        def weighted_neighbors(node):
            graph = {
                'A': [('B', 1), ('C', 4)],
                'B': [('C', 2), ('D', 5)],
                'C': [('D', 1)],
                'D': []
            }
            return graph.get(node, [])

        distances = dijkstra('A', weighted_neighbors)
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 1)
        self.assertEqual(distances['C'], 3)  # A->B->C is shorter than A->C
        self.assertEqual(distances['D'], 4)  # A->B->C->D

    def test_dijkstra_with_goal(self):
        """Test Dijkstra with specific goal."""
        def weighted_neighbors(node):
            graph = {
                'A': [('B', 1), ('C', 4)],
                'B': [('C', 2), ('D', 5)],
                'C': [('D', 1)],
                'D': []
            }
            return graph.get(node, [])

        # dijkstra returns dict even with goal parameter
        distances = dijkstra('A', weighted_neighbors, goal='D')
        self.assertIsInstance(distances, dict)
        self.assertEqual(distances['D'], 4)

    def test_find_max_clique(self):
        """Test maximum clique finding."""
        # Triangle: A-B-C all connected
        graph = {
            'A': {'B', 'C'},
            'B': {'A', 'C'},
            'C': {'A', 'B'},
            'D': {'A'}  # D only connected to A
        }

        clique = find_max_clique(graph)
        self.assertEqual(len(clique), 3)
        self.assertTrue(clique.issubset({'A', 'B', 'C'}))

    def test_bfs_unreachable(self):
        """Test BFS with unreachable goal."""
        def neighbors(node):
            return {'A': ['B'], 'B': [], 'C': []}.get(node, [])

        def goal(node):
            return node == 'C'

        path = bfs('A', neighbors, goal)
        # BFS returns empty list [] when goal is unreachable
        self.assertEqual(path, [])


if __name__ == "__main__":
    unittest.main()
