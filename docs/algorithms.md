# Graph Algorithms

[← Back to README](../README.md)

The `aoc.graph` module provides generic graph algorithms that work with any hashable state type (coordinates, tuples, strings, etc.).

## Table of Contents

- [BFS (Breadth-First Search)](#bfs-breadth-first-search)
- [DFS (Depth-First Search)](#dfs-depth-first-search)
- [DFS Grid Path](#dfs-grid-path)
- [Dijkstra's Algorithm](#dijkstras-algorithm)
- [Maximum Clique](#maximum-clique)
- [Examples](#examples)

---

## BFS (Breadth-First Search)

Finds shortest paths in unweighted graphs.

```python
def bfs(
    start: Hashable,
    neighbors_func: Callable[[Hashable], list[Hashable]],
    goal_func: Callable[[Hashable], bool] | None = None
) -> dict[Hashable, int] | list[Hashable] | None
```

**Parameters:**
- `start`: Starting state (any hashable type)
- `neighbors_func`: Function returning list of neighbors for a state
- `goal_func`: Optional goal test function

**Returns:**
- If `goal_func` is None: `dict[state, distance]` for all reachable states
- If `goal_func` provided: `list[state]` path to goal, or `None` if not found

### Mode 1: All Distances (No Goal)

```python
from aoc import bfs

# Define neighbor function
def neighbors(state):
    # Return list of neighbor states
    return [neighbor1, neighbor2, ...]

# Get distances to all reachable states
distances = bfs(start_state, neighbors)
# {state1: 0, state2: 1, state3: 2, ...}

# Check specific distance
if target in distances:
    print(f"Distance to target: {distances[target]}")
```

**Example - Grid BFS:**
```python
from aoc import bfs, Coord, read_data_as_char_grid, grid_max_bounds, grid_get

grid = read_data_as_char_grid("maze")
max_bounds = grid_max_bounds(grid)
start = Coord(0, 0)

def neighbors(pos):
    valid_neighbors = []
    for direction in Coord.DIRECTIONS_CARDINAL:
        next_pos = pos + direction
        if next_pos.in_bounds(max_bounds) and grid_get(grid, next_pos) != '#':
            valid_neighbors.append(next_pos)
    return valid_neighbors

distances = bfs(start, neighbors)
# {Coord(0,0): 0, Coord(0,1): 1, Coord(1,0): 1, ...}
```

### Mode 2: Path to Goal

```python
from aoc import bfs

def goal_test(state):
    return state == target_state

path = bfs(start, neighbors, goal_test)
if path:
    print(f"Found path: {path}")
    print(f"Path length: {len(path) - 1}")
else:
    print("No path found")
```

**Example - Maze Path:**
```python
from aoc import bfs, find_first

start = find_first(grid, 'S')
end = find_first(grid, 'E')

def is_goal(pos):
    return pos == end

path = bfs(start, neighbors, is_goal)
# [Coord(0,0), Coord(0,1), Coord(1,1), ..., end]
```

---

## DFS (Depth-First Search)

Finds any path to goal using depth-first exploration.

```python
def dfs(
    start: Hashable,
    neighbors_func: Callable[[Hashable], list[Hashable]],
    goal_func: Callable[[Hashable], bool]
) -> list[Hashable] | None
```

**Parameters:**
- `start`: Starting state
- `neighbors_func`: Function returning neighbors
- `goal_func`: Goal test function (required)

**Returns:**
- `list[state]` path from start to goal, or `None` if not found

**Note:** DFS finds **a** path, not necessarily the **shortest** path. Use BFS for shortest paths.

```python
from aoc import dfs

def neighbors(state):
    return [neighbor1, neighbor2, ...]

def is_goal(state):
    return state == target

path = dfs(start, neighbors, is_goal)
if path:
    print(f"Found path of length {len(path) - 1}")
```

**Use cases:**
- Puzzle solving (find any solution)
- Maze exploration (any path works)
- When path optimality doesn't matter

---

## DFS Grid Path

Convenience wrapper for grid-based pathfinding.

```python
def dfs_grid_path(
    grid: list[list[Any]],
    start: Coord,
    end: Coord,
    walkable_values: set[Any],
    directions: list[Coord] = Coord.DIRECTIONS_CARDINAL
) -> list[Coord] | None
```

**Parameters:**
- `grid`: 2D grid
- `start`: Starting coordinate
- `end`: Target coordinate
- `walkable_values`: Set of cell values that can be traversed
- `directions`: Movement directions (default: cardinal)

**Returns:**
- `list[Coord]` path from start to end, or `None`

```python
from aoc import dfs_grid_path, Coord, read_data_as_char_grid, find_first

grid = read_data_as_char_grid("maze")
start = find_first(grid, 'S')
end = find_first(grid, 'E')

# Find path through '.', 'S', and 'E' cells
path = dfs_grid_path(grid, start, end, walkable_values={'.', 'S', 'E'})

if path:
    print(f"Path length: {len(path) - 1}")
    for pos in path:
        print(f"  Step: {pos}")
```

**With diagonal movement:**
```python
path = dfs_grid_path(
    grid, start, end,
    walkable_values={'.', 'S', 'E'},
    directions=Coord.DIRECTIONS_ALL  # Include diagonals
)
```

---

## Dijkstra's Algorithm

Finds shortest paths in weighted graphs.

```python
def dijkstra(
    start: Hashable,
    neighbors_func: Callable[[Hashable], list[tuple[Hashable, int]]],
    goal: Hashable | None = None
) -> dict[Hashable, int] | int | None
```

**Parameters:**
- `start`: Starting state
- `neighbors_func`: Returns `list[(neighbor_state, cost)]`
- `goal`: Optional target state

**Returns:**
- If `goal` is None: `dict[state, distance]` for all reachable states
- If `goal` provided: `int` distance to goal, or `None` if unreachable

### Mode 1: All Shortest Distances

```python
from aoc import dijkstra

def weighted_neighbors(state):
    # Return list of (neighbor, cost) tuples
    return [
        (neighbor1, cost1),
        (neighbor2, cost2),
        ...
    ]

distances = dijkstra(start, weighted_neighbors)
# {state1: 0, state2: 5, state3: 12, ...}
```

**Example - Weighted Grid:**
```python
from aoc import dijkstra, Coord, read_data_as_int_grid, grid_max_bounds, grid_get

grid = read_data_as_int_grid("costs")  # Each cell has movement cost
max_bounds = grid_max_bounds(grid)
start = Coord(0, 0)

def weighted_neighbors(pos):
    neighbors = []
    for direction in Coord.DIRECTIONS_CARDINAL:
        next_pos = pos + direction
        if next_pos.in_bounds(max_bounds):
            cost = grid_get(grid, next_pos)  # Cell value is cost
            neighbors.append((next_pos, cost))
    return neighbors

distances = dijkstra(start, weighted_neighbors)
# {Coord(0,0): 0, Coord(0,1): 3, Coord(1,0): 5, ...}
```

### Mode 2: Distance to Specific Goal

```python
from aoc import dijkstra

goal_state = Coord(9, 9)

distance = dijkstra(start, weighted_neighbors, goal=goal_state)

if distance is not None:
    print(f"Shortest distance to goal: {distance}")
else:
    print("Goal unreachable")
```

### Variable Cost Example

```python
def neighbors_with_costs(pos):
    neighbors = []
    for direction in Coord.DIRECTIONS_CARDINAL:
        next_pos = pos + direction
        if next_pos.in_bounds(max_bounds):
            # Different costs based on direction
            if direction == Coord.UP:
                cost = 1  # Uphill is cheap
            else:
                cost = 2  # Other directions cost more
            neighbors.append((next_pos, cost))
    return neighbors

distances = dijkstra(start, neighbors_with_costs)
```

---

## Maximum Clique

Finds largest clique in undirected graph using Bron-Kerbosch algorithm.

```python
def find_max_clique(
    graph: dict[Hashable, set[Hashable]]
) -> set[Hashable]
```

**Parameters:**
- `graph`: Adjacency dictionary `{node: {neighbors}}`

**Returns:**
- `set` of nodes forming maximum clique (empty set if graph is empty)

**Definition:** A clique is a subset of nodes where every pair is connected.

```python
from aoc import find_max_clique

# Graph representation: adjacency dict
graph = {
    'A': {'B', 'C', 'D'},
    'B': {'A', 'C'},
    'C': {'A', 'B', 'D'},
    'D': {'A', 'C'},
}

clique = find_max_clique(graph)
# {'A', 'C', 'D'} - largest fully connected group

print(f"Max clique size: {len(clique)}")
print(f"Nodes: {clique}")
```

**Example - Network Analysis:**
```python
from aoc import read_data_as_graph_edges, find_max_clique

# File format: "A-B\nB-C\n..."
graph = read_data_as_graph_edges("connections")
clique = find_max_clique(graph)

print(f"Largest interconnected group: {clique}")
```

**Properties:**
- Works with any hashable node type (strings, ints, tuples, Coord, etc.)
- Graph must be undirected (if A→B, then B→A)
- Computationally expensive for large graphs (NP-complete)
- Returns empty set for empty graphs

---

## Examples

### Example 1: BFS Shortest Path (Grid)

```python
from aoc import (
    bfs, read_data_as_char_grid,
    find_first, grid_max_bounds, grid_get,
    Coord
)

def solve_maze(data_file):
    grid = read_data_as_char_grid(data_file)
    start = find_first(grid, 'S')
    end = find_first(grid, 'E')
    max_bounds = grid_max_bounds(grid)

    def neighbors(pos):
        result = []
        for direction in Coord.DIRECTIONS_CARDINAL:
            next_pos = pos + direction
            if (next_pos.in_bounds(max_bounds) and
                grid_get(grid, next_pos) in {'.', 'S', 'E'}):
                result.append(next_pos)
        return result

    def is_end(pos):
        return pos == end

    path = bfs(start, neighbors, is_end)
    return len(path) - 1 if path else -1
```

### Example 2: Dijkstra with State Tuples

```python
from aoc import dijkstra, Coord

def solve_with_keys(data_file):
    # State: (position, keys_collected)
    start_state = (Coord(0, 0), frozenset())

    def neighbors(state):
        pos, keys = state
        neighbors = []

        for direction in Coord.DIRECTIONS_CARDINAL:
            next_pos = pos + direction
            cell = grid_get(grid, next_pos)

            if cell == '#':
                continue  # Wall

            new_keys = keys
            cost = 1

            if cell.isupper():  # Door
                if cell.lower() not in keys:
                    continue  # Can't pass without key
            elif cell.islower():  # Key
                new_keys = keys | {cell}  # Collect key

            new_state = (next_pos, new_keys)
            neighbors.append((new_state, cost))

        return neighbors

    goal_pos = find_first(grid, 'E')
    distances = dijkstra(start_state, neighbors)

    # Find minimum distance to goal with any key combination
    min_dist = float('inf')
    for (pos, keys), dist in distances.items():
        if pos == goal_pos:
            min_dist = min(min_dist, dist)

    return min_dist if min_dist != float('inf') else -1
```

### Example 3: Network Analysis with Cliques

```python
from aoc import read_data_as_graph_edges, find_max_clique

def analyze_network(data_file):
    # Build graph from edges
    graph = read_data_as_graph_edges(data_file)

    # Find largest fully-connected group
    largest_group = find_max_clique(graph)

    print(f"Largest interconnected group:")
    print(f"  Size: {len(largest_group)}")
    print(f"  Members: {sorted(largest_group)}")

    # Find all nodes connected to every member of the group
    connected_to_all = set(graph.keys())
    for member in largest_group:
        connected_to_all &= graph[member]

    print(f"  Nodes connected to entire group: {connected_to_all - largest_group}")

    return largest_group
```

### Example 4: DFS vs BFS Comparison

```python
from aoc import bfs, dfs, Coord

def compare_algorithms(grid, start, end, neighbors_func):
    # DFS - finds any path quickly
    def is_goal(pos):
        return pos == end

    dfs_path = dfs(start, neighbors_func, is_goal)
    print(f"DFS path length: {len(dfs_path) - 1 if dfs_path else 'No path'}")

    # BFS - finds shortest path
    bfs_path = bfs(start, neighbors_func, is_goal)
    print(f"BFS path length: {len(bfs_path) - 1 if bfs_path else 'No path'}")

    # BFS distance map
    distances = bfs(start, neighbors_func)
    if end in distances:
        print(f"BFS distance to end: {distances[end]}")
```

### Example 5: Multi-Goal Dijkstra

```python
from aoc import dijkstra, Coord

def find_closest_goal(grid, start, goal_positions):
    """Find closest goal among multiple targets."""

    def weighted_neighbors(pos):
        neighbors = []
        for direction in Coord.DIRECTIONS_CARDINAL:
            next_pos = pos + direction
            if next_pos.in_bounds(max_bounds):
                cost = grid_get(grid, next_pos)  # Use grid values as costs
                neighbors.append((next_pos, cost))
        return neighbors

    distances = dijkstra(start, weighted_neighbors)

    # Find closest goal
    min_distance = float('inf')
    closest_goal = None

    for goal in goal_positions:
        if goal in distances and distances[goal] < min_distance:
            min_distance = distances[goal]
            closest_goal = goal

    return closest_goal, min_distance
```

## Performance Considerations

### BFS
- **Time**: O(V + E) where V = vertices, E = edges
- **Space**: O(V) for queue and visited set
- **Best for**: Unweighted graphs, shortest path needed

### DFS
- **Time**: O(V + E)
- **Space**: O(V) for stack and visited set
- **Best for**: Any path acceptable, memory constrained, detecting cycles

### Dijkstra
- **Time**: O((V + E) log V) with heap
- **Space**: O(V) for priority queue and distances
- **Best for**: Weighted graphs, shortest path by cost

### Max Clique
- **Time**: Exponential in worst case (NP-complete)
- **Space**: O(V) for recursion
- **Best for**: Small to medium graphs (<50 nodes), when clique size needed

---

[← Back to README](../README.md) | [Next: Migration →](migration.md)
