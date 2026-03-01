import pygame
import sys
from grid import Grid, EMPTY, WALL, START, GOAL
from algorithms import gbfs, astar, manhattan, euclidean

# Window and Grid Settings
CELL_SIZE    = 40
SIDEBAR_W    = 260
FPS          = 60

# Colors
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
GRAY       = (200, 200, 200)
DARK_GRAY  = (50,  50,  50 )
GREEN      = (0,   200, 0  )
RED        = (220, 50,  50 )
BLUE       = (50,  50,  220)
YELLOW     = (255, 220, 0  )
ORANGE     = (255, 140, 0  )
TEAL       = (0,   180, 180)
PURPLE     = (150, 0,   200)
BG_COLOR   = (30,  30,  30 )
PANEL_COLOR= (45,  45,  45 )

# Cell Colors
CELL_COLORS = {
    EMPTY : WHITE,
    WALL  : DARK_GRAY,
    START : GREEN,
    GOAL  : RED,
}


class Button:

    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect        = pygame.Rect(x, y, w, h)
        self.text        = text
        self.color       = color
        self.hover_color = hover_color
        self.active      = False

    def draw(self, surface, font):
        mouse = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse) else self.color
        if self.active:
            color = ORANGE
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=6)
        label = font.render(self.text, True, WHITE)
        lx = self.rect.x + (self.rect.w - label.get_width())  // 2
        ly = self.rect.y + (self.rect.h - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class Visualizer:

    def __init__(self, rows=15, cols=15):
        pygame.init()
        self.rows = rows
        self.cols = cols

        # Window size = grid area + sidebar
        self.grid_w  = cols * CELL_SIZE
        self.grid_h  = rows * CELL_SIZE
        self.win_w   = self.grid_w + SIDEBAR_W
        self.win_h   = max(self.grid_h, 620)

        self.screen  = pygame.display.set_mode((self.win_w, self.win_h))
        pygame.display.set_caption("AI2002 - Dynamic Pathfinding Agent")

        self.clock   = pygame.time.Clock()
        self.font_sm = pygame.font.SysFont("consolas", 13)
        self.font_md = pygame.font.SysFont("consolas", 15, bold=True)
        self.font_lg = pygame.font.SysFont("consolas", 17, bold=True)

        self.grid    = Grid(rows, cols)

        # State
        self.path          = []
        self.visited_nodes = set()
        self.frontier_nodes= set()
        self.result_cost   = 0
        self.result_time   = 0
        self.result_count  = 0
        self.message       = "Draw walls or generate a map, then run."
        self.dynamic_mode  = False
        self.agent_pos     = None
        self.agent_index   = 0

        # Selected algorithm and heuristic
        self.algo      = "astar"      # "astar" or "gbfs"
        self.heuristic = "manhattan"  # "manhattan" or "euclidean"

        self._build_buttons()

    def _build_buttons(self):
        # Builds all sidebar buttons
        sx = self.grid_w + 10
        bw = SIDEBAR_W - 20
        bh = 32

        self.btn_astar     = Button(sx, 60,  bw, bh, "A* Search",         BLUE,     (80, 80, 200))
        self.btn_gbfs      = Button(sx, 100, bw, bh, "Greedy BFS",         BLUE,     (80, 80, 200))
        self.btn_manhattan = Button(sx, 160, bw, bh, "Manhattan",          TEAL,     (0, 140, 140))
        self.btn_euclidean = Button(sx, 200, bw, bh, "Euclidean",          TEAL,     (0, 140, 140))
        self.btn_run       = Button(sx, 260, bw, bh, "Run Search",         GREEN,    (0, 160, 0  ))
        self.btn_dynamic   = Button(sx, 300, bw, bh, "Dynamic Mode",       PURPLE,   (120, 0, 170))
        self.btn_random    = Button(sx, 360, bw, bh, "Random Map (30%)",   ORANGE,   (200, 110, 0))
        self.btn_clear     = Button(sx, 400, bw, bh, "Clear Grid",         DARK_GRAY,(80, 80, 80 ))
        self.btn_reset_vis = Button(sx, 440, bw, bh, "Reset Visuals",      DARK_GRAY,(80, 80, 80 ))

        self.btn_astar.active     = True
        self.btn_manhattan.active = True

        self.all_buttons = [
            self.btn_astar, self.btn_gbfs,
            self.btn_manhattan, self.btn_euclidean,
            self.btn_run, self.btn_dynamic,
            self.btn_random, self.btn_clear, self.btn_reset_vis
        ]

    def _get_heuristic_fn(self):
        return manhattan if self.heuristic == "manhattan" else euclidean

    def _run_search(self):
        import time
        fn = self._get_heuristic_fn()
        t0 = time.time()
        if self.algo == "astar":
            path, cost, visited, frontier = astar(self.grid, fn)
        else:
            path, cost, visited, frontier = gbfs(self.grid, fn)
        t1 = time.time()

        self.path           = path if path else []
        self.visited_nodes  = visited
        self.frontier_nodes = frontier
        self.result_cost    = cost
        self.result_time    = round((t1 - t0) * 1000, 2)
        self.result_count   = len(visited)

        if path:
            self.message = "Path found!"
            self.agent_pos   = self.grid.start
            self.agent_index = 0
        else:
            self.message = "No path found!"

    def _draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell  = self.grid.cells[row][col]
                color = CELL_COLORS.get(cell, WHITE)
                pos   = (row, col)

                # Overlay search visualization colors
                if cell not in (START, GOAL):
                    if pos in self.visited_nodes:
                        color = BLUE
                    if pos in self.frontier_nodes:
                        color = YELLOW
                    if self.path and pos in self.path:
                        color = GREEN

                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

        # Draw agent as a circle when animating
        if self.agent_pos:
            r, c = self.agent_pos
            cx   = c * CELL_SIZE + CELL_SIZE // 2
            cy   = r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.screen, ORANGE, (cx, cy), CELL_SIZE // 3)

    def _draw_sidebar(self):
        sx = self.grid_w
        pygame.draw.rect(self.screen, PANEL_COLOR, (sx, 0, SIDEBAR_W, self.win_h))

        # Title
        title = self.font_lg.render("Pathfinding Agent", True, WHITE)
        self.screen.blit(title, (sx + 10, 15))

        # Section labels
        self.screen.blit(self.font_md.render("Algorithm:", True, GRAY),  (sx + 10, 45))
        self.screen.blit(self.font_md.render("Heuristic:", True, GRAY),  (sx + 10, 145))
        self.screen.blit(self.font_md.render("Controls:", True, GRAY),   (sx + 10, 245))
        self.screen.blit(self.font_md.render("Map Editor:", True, GRAY), (sx + 10, 345))

        # Draw all buttons
        for btn in self.all_buttons:
            btn.draw(self.screen, self.font_sm)

        # Metrics
        my = 495
        self.screen.blit(self.font_md.render("Metrics:", True, GRAY), (sx + 10, my))
        metrics = [
            f"Nodes Visited : {self.result_count}",
            f"Path Cost     : {self.result_cost}",
            f"Time (ms)     : {self.result_time}",
        ]
        for i, m in enumerate(metrics):
            self.screen.blit(self.font_sm.render(m, True, WHITE), (sx + 10, my + 20 + i * 18))

        # Message
        self.screen.blit(self.font_sm.render(self.message, True, YELLOW), (sx + 10, self.win_h - 30))

    def _handle_buttons(self, event):
        if self.btn_astar.is_clicked(event):
            self.algo = "astar"
            self.btn_astar.active = True
            self.btn_gbfs.active  = False

        if self.btn_gbfs.is_clicked(event):
            self.algo = "gbfs"
            self.btn_gbfs.active  = True
            self.btn_astar.active = False

        if self.btn_manhattan.is_clicked(event):
            self.heuristic = "manhattan"
            self.btn_manhattan.active = True
            self.btn_euclidean.active = False

        if self.btn_euclidean.is_clicked(event):
            self.heuristic = "euclidean"
            self.btn_euclidean.active = True
            self.btn_manhattan.active = False

        if self.btn_run.is_clicked(event):
            self._reset_visuals()
            self._run_search()

        if self.btn_dynamic.is_clicked(event):
            # Toggle dynamic mode on/off
            self.dynamic_mode = not self.dynamic_mode
            self.btn_dynamic.active = self.dynamic_mode
            self.message = "Dynamic Mode ON" if self.dynamic_mode else "Dynamic Mode OFF"

        if self.btn_random.is_clicked(event):
            self._reset_visuals()
            self.grid.generate_random_map(density=0.3)
            self.message = "Random map generated."

        if self.btn_clear.is_clicked(event):
            self._reset_visuals()
            self.grid.reset()
            self.message = "Grid cleared."

        if self.btn_reset_vis.is_clicked(event):
            self._reset_visuals()

    def _reset_visuals(self):
        self.path           = []
        self.visited_nodes  = set()
        self.frontier_nodes = set()
        self.result_cost    = 0
        self.result_time    = 0
        self.result_count   = 0
        self.agent_pos      = None
        self.agent_index    = 0
        self.message        = "Visuals reset."

    def _handle_grid_click(self, event):
        # Toggle walls by clicking on grid cells
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if mx < self.grid_w:
                col = mx // CELL_SIZE
                row = my // CELL_SIZE
                if self.grid.is_valid(row, col):
                    self.grid.toggle_wall(row, col)
                    self._reset_visuals()

    def _animate_agent(self):
        # Moves agent one step along the path per frame in dynamic mode
        if not self.path or self.agent_index >= len(self.path):
            self.agent_pos = None
            return

        self.agent_pos    = self.path[self.agent_index]
        self.agent_index += 1

        if self.dynamic_mode:
            remaining = self.path[self.agent_index:]
            new_wall  = self.grid.spawn_dynamic_obstacle(remaining, spawn_probability=0.5)
            if new_wall and new_wall in set(remaining):
                # Obstacle on path — replan from current position
                self.message = f"Obstacle at {new_wall}! Replanning..."
                temp_start        = self.grid.start
                self.grid.start   = self.agent_pos
                fn                = self._get_heuristic_fn()
                if self.algo == "astar":
                    path, cost, visited, frontier = astar(self.grid, fn)
                else:
                    path, cost, visited, frontier = gbfs(self.grid, fn)
                self.grid.start = temp_start

                if path:
                    self.path           = path
                    self.agent_index    = 1
                    self.visited_nodes  = visited
                    self.frontier_nodes = frontier
                    self.result_cost    = cost
                    self.result_count   = len(visited)
                else:
                    self.message  = "No path after replanning!"
                    self.agent_pos = None

    def run(self):
        # Main game loop
        animating = False
        anim_timer = 0

        while True:
            self.clock.tick(FPS)
            anim_timer += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_buttons(event)
                self._handle_grid_click(event)

                # Start animation when run is clicked and path exists
                if self.btn_run.is_clicked(event) and self.path:
                    animating  = True
                    anim_timer = 0

            # Animate agent every 10 frames
            if animating and self.path:
                if anim_timer % 20 == 0:
                    self._animate_agent()
                if self.agent_pos is None:
                    animating = False

            self.screen.fill(BG_COLOR)
            self._draw_grid()
            self._draw_sidebar()
            pygame.display.flip()


if __name__ == "__main__":
    v = Visualizer(rows=15, cols=15)
    v.run()