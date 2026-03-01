import random

# Cell Type Constants
EMPTY = 0
WALL  = 1
START = 2
GOAL  = 3


class Grid:

    def __init__(self, rows, cols):
        # Creates a blank grid, fixes start at top-left and goal at bottom-right
        self.rows = rows
        self.cols = cols
        self.cells = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.goal  = (rows - 1, cols - 1)
        self.cells[self.start[0]][self.start[1]] = START
        self.cells[self.goal[0]][self.goal[1]]   = GOAL

    def is_wall(self, row, col):
        # Returns True if the cell is a wall
        return self.cells[row][col] == WALL

    def is_walkable(self, row, col):
        # Returns True if the cell is inside the grid and not a wall
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= self.cols:
            return False
        return self.cells[row][col] != WALL

    def is_valid(self, row, col):
        # Returns True if (row, col) is inside grid boundaries
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_wall(self, row, col):
        # Places a wall at (row, col), start and goal are protected
        if (row, col) == self.start or (row, col) == self.goal:
            return
        self.cells[row][col] = WALL

    def remove_wall(self, row, col):
        # Removes a wall and makes the cell empty again
        if (row, col) == self.start or (row, col) == self.goal:
            return
        if self.cells[row][col] == WALL:
            self.cells[row][col] = EMPTY

    def toggle_wall(self, row, col):
        # Flips a cell between EMPTY and WALL when user clicks on it
        if (row, col) == self.start or (row, col) == self.goal:
            return
        if self.cells[row][col] == WALL:
            self.cells[row][col] = EMPTY
        elif self.cells[row][col] == EMPTY:
            self.cells[row][col] = WALL

    def generate_random_map(self, density=0.3):
        # Fills the grid with random walls based on density (0.3 = 30% walls)
        self.cells = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) == self.start or (row, col) == self.goal:
                    continue
                if random.random() < density:
                    self.cells[row][col] = WALL
        self.cells[self.start[0]][self.start[1]] = START
        self.cells[self.goal[0]][self.goal[1]]   = GOAL

    def reset(self):
        # Clears the entire grid back to blank, keeps start and goal
        self.cells = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells[self.start[0]][self.start[1]] = START
        self.cells[self.goal[0]][self.goal[1]]   = GOAL

    def get_neighbours(self, row, col):
        # Returns all walkable cells adjacent to (row, col) with cost 1
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbours = []
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            if self.is_walkable(new_row, new_col):
                neighbours.append((new_row, new_col, 1))
        return neighbours

    def spawn_dynamic_obstacle(self, current_path, spawn_probability=0.05):
        # Randomly places a new wall during dynamic mode, never on the current path
        if random.random() > spawn_probability:
            return None
        candidates = []
        path_set = set(current_path) if current_path else set()
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in path_set:
                    continue
                if (row, col) == self.start or (row, col) == self.goal:
                    continue
                if self.cells[row][col] == EMPTY:
                    candidates.append((row, col))
        if not candidates:
            return None
        chosen = random.choice(candidates)
        self.cells[chosen[0]][chosen[1]] = WALL
        return chosen

    def print_grid(self):
        # Prints the grid in terminal using S, G, #, and . symbols
        symbols = {EMPTY: '.', WALL: '#', START: 'S', GOAL: 'G'}
        for row in self.cells:
            print(' '.join(symbols[cell] for cell in row))
        print()


if __name__ == "__main__":
    print("=== Testing Grid (5x5, 30% obstacles) ===\n")
    g = Grid(5, 5)
    g.generate_random_map(density=0.3)
    g.print_grid()
    print("Start:", g.start)
    print("Goal: ", g.goal)
    print("Neighbours of Start:", g.get_neighbours(0, 0))