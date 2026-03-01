import time


class Metrics:

    def __init__(self):
        self.nodes_visited = 0
        self.path_cost     = 0
        self.start_time    = 0
        self.end_time      = 0
        self.execution_ms  = 0

    def start_timer(self):
        # Call this just before running the search algorithm
        self.start_time = time.time()

    def stop_timer(self):
        # Call this right after the search algorithm finishes
        self.end_time     = time.time()
        self.execution_ms = round((self.end_time - self.start_time) * 1000, 2)

    def update(self, nodes_visited, path_cost):
        # Updates node count and path cost after search completes
        self.nodes_visited = nodes_visited
        self.path_cost     = path_cost

    def reset(self):
        # Clears all metrics back to zero
        self.nodes_visited = 0
        self.path_cost     = 0
        self.start_time    = 0
        self.end_time      = 0
        self.execution_ms  = 0

    def get_summary(self):
        # Returns a dictionary of all metrics for easy access
        return {
            "Nodes Visited" : self.nodes_visited,
            "Path Cost"     : self.path_cost,
            "Time (ms)"     : self.execution_ms,
        }

    def print_summary(self):
        print("===== Search Metrics =====")
        for key, val in self.get_summary().items():
            print(f"  {key:15} : {val}")
        print("==========================")


if __name__ == "__main__":
    from grid import Grid
    from algorithms import astar, manhattan

    m = Metrics()
    g = Grid(10, 10)
    g.generate_random_map(density=0.2)

    m.start_timer()
    path, cost, visited, frontier = astar(g, manhattan)
    m.stop_timer()
    m.update(len(visited), cost)
    m.print_summary()