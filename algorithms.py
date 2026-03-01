import heapq

# Heuristic Functions

def manhattan(a, b):
    # Sum of horizontal and vertical distance between two cells
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    # Straight line distance between two cells
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Path Reconstruction

def reconstruct_path(came_from, start, goal):
    # Traces back from goal to start using the came_from dictionary
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


# Greedy Best First Search

def gbfs(grid, heuristic_fn):
    start = grid.start
    goal  = grid.goal

    # Priority queue stores (h(n), node)
    frontier = []
    heapq.heappush(frontier, (heuristic_fn(start, goal), start))

    came_from  = {start: None}
    visited    = set()
    visited.add(start)

    frontier_nodes  = set()
    visited_nodes   = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        visited_nodes.add(current)
        frontier_nodes.discard(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            cost = len(path) - 1
            return path, cost, visited_nodes, frontier_nodes

        for row, col, _ in grid.get_neighbours(current[0], current[1]):
            neighbour = (row, col)
            if neighbour not in visited:
                visited.add(neighbour)
                came_from[neighbour] = current
                h = heuristic_fn(neighbour, goal)
                heapq.heappush(frontier, (h, neighbour))
                frontier_nodes.add(neighbour)

    return None, 0, visited_nodes, frontier_nodes


# A* Search

def astar(grid, heuristic_fn):
    start = grid.start
    goal  = grid.goal

    # Priority queue stores (f(n), g(n), node)
    frontier = []
    heapq.heappush(frontier, (0, 0, start))

    came_from  = {start: None}
    g_cost     = {start: 0}
    expanded   = set()

    frontier_nodes = set()
    visited_nodes  = set()

    while frontier:
        f, g, current = heapq.heappop(frontier)

        if current in expanded:
            continue

        expanded.add(current)
        visited_nodes.add(current)
        frontier_nodes.discard(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            cost = g_cost[goal]
            return path, cost, visited_nodes, frontier_nodes

        for row, col, step_cost in grid.get_neighbours(current[0], current[1]):
            neighbour = (row, col)
            new_g = g + step_cost

            if neighbour not in g_cost or new_g < g_cost[neighbour]:
                g_cost[neighbour]    = new_g
                came_from[neighbour] = current
                h = heuristic_fn(neighbour, goal)
                f = new_g + h
                heapq.heappush(frontier, (f, new_g, neighbour))
                frontier_nodes.add(neighbour)

    return None, 0, visited_nodes, frontier_nodes


if __name__ == "__main__":
    from grid import Grid

    print("=== Testing Algorithms (10x10, 20% obstacles) ===\n")
    g = Grid(10, 10)
    g.generate_random_map(density=0.2)
    g.print_grid()

    print("--- GBFS (Manhattan) ---")
    path, cost, visited, frontier = gbfs(g, manhattan)
    if path:
        print("Path:", path)
        print("Cost:", cost)
        print("Nodes visited:", len(visited))
    else:
        print("No path found")

    print("\n--- A* (Manhattan) ---")
    path, cost, visited, frontier = astar(g, manhattan)
    if path:
        print("Path:", path)
        print("Cost:", cost)
        print("Nodes visited:", len(visited))
    else:
        print("No path found")