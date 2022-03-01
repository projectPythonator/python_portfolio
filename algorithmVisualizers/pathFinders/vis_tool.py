import pygame

NESW = [(-1, 0), (0, -1), (1, 0), (0, 1)]

GRID_ROWS: int = 50
GRID_COLS: int = 50
GRID_WIDTH: int = 800
GRID_HEIGHT: int = 800
CELL_WIDTH: int = GRID_WIDTH // GRID_COLS
CELL_HEIGHT: int = GRID_HEIGHT // GRID_ROWS

COLOURS: dict = {}


def fill_colours():
    global COLOURS
    COLOURS["RED"] = (255, 0, 0)
    COLOURS["GREEN"] = (0, 255, 0)
    COLOURS["BLUE"] = (0, 0, 255)
    COLOURS["YELLOW"] = (255, 255, 0)
    COLOURS["WHITE"] = (255, 255, 255)
    COLOURS["BLACK"] = (0, 0, 0)
    COLOURS["PURPLE"] = (128, 0, 128)
    COLOURS["ORANGE"] = (255, 165, 0)
    COLOURS["GREY"] = (128, 128, 128)
    COLOURS["TURQUOISE"] = (64, 224, 208)


class GridCell:
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col
        self.cell_x: int = col * CELL_WIDTH
        self.cell_y: int = row * CELL_HEIGHT
        self.cell_colour = COLOURS["WHITE"]
        self.cell_neighbours = []

    def get_pos(self):
        return (self.row, self.col)

    def is_closed(self) -> bool:
        return self.cell_colour == COLOURS["RED"]

    def is_open(self) -> bool:
        return self.cell_colour == COLOURS["GREEN"]

    def is_barrier(self) -> bool:
        return self.cell_colour == COLOURS["BLACK"]

    def is_start(self) -> bool:
        return self.cell_colour == COLOURS["ORANGE"]

    def is_end(self) -> bool:
        return self.cell_colour == COLOURS["TURQUOISE"]

    def reset(self):
        self.cell_colour = COLOURS["WHITE"]

    def make_closed(self):
        self.cell_colour = COLOURS["RED"]

    def make_open(self):
        self.cell_colour = COLOURS["GREEN"]

    def make_barrier(self):
        self.cell_colour = COLOURS["BLACK"]

    def make_start(self):
        self.cell_colour = COLOURS["ORANGE"]

    def make_end(self):
        self.cell_colour = COLOURS["TURQUOISE"]

    def make_path(self):
        self.cell_colour = COLOURS["PURPLE"]

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.cell_colour,
            (self.cell_x, self.cell_y, CELL_WIDTH, CELL_HEIGHT),
        )

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.is_barrier():
            return
        for r, c in NESW:  # loop north east south west
            new_row, new_col = self.row + r, self.col + c
            if not grid[new_row][new_col].is_barrier():
                self.neighbours.append(grid[new_row][new_col])

    def __lt__(self, other):
        return False


class Visualizer:
    def __init__(self, width: int, height: int, display_name: str):
        self.WINDOW = pygame.display.set_mode((width, height))
        pygame.display.set_caption(display_name)
        self.grid = []
        self.start_cell = None
        self.end_cell = None

    def make_grid(self):
        self.grid = []
        for row in range(GRID_ROWS):
            self.grid.append([])
            for col in range(GRID_COLS):
                cell = GridCell(row, col)
                self.grid[row].append(cell)
        for row in range(GRID_ROWS):
            self.grid[row][0].make_barrier()
            self.grid[row][GRID_COLS - 1].make_barrier()
        for col in range(GRID_COLS):
            self.grid[0][col].make_barrier()
            self.grid[GRID_ROWS - 1][col].make_barrier()

    def draw_grid(self):
        for row in range(GRID_ROWS):
            pygame.draw.line(
                self.WINDOW,
                COLOURS["GREY"],
                (0, row * CELL_WIDTH),
                (GRID_WIDTH, row * CELL_WIDTH),
            )
        for col in range(GRID_COLS):
            pygame.draw.line(
                self.WINDOW,
                COLOURS["GREY"],
                (col * CELL_HEIGHT, 0),
                (col * CELL_HEIGHT, GRID_HEIGHT),
            )

    def draw(self):
        self.WINDOW.fill(COLOURS["WHITE"])
        for row in self.grid:
            for cell in row:
                cell.draw(self.WINDOW)
        self.draw_grid()
        pygame.display.update()

    def get_clicked_pos(self, pos):
        x, y = pos
        row = y // CELL_HEIGHT
        col = x // CELL_WIDTH
        return row, col

    def left_click_event(self, pos):
        row, col = self.get_clicked_pos(pos)
        if not (1 <= row < (GRID_ROWS - 1) and 1 <= col < (GRID_COLS - 1)):
            return
        cur_cell: GridCell = self.grid[row][col]
        if not self.start_cell and cur_cell != self.end_cell:
            self.start_cell = cur_cell
            cur_cell.make_start()
            return
        elif not self.end_cell and cur_cell != self.start_cell:
            self.end_cell = cur_cell
            cur_cell.make_end()
        elif cur_cell != self.end_cell and cur_cell != self.start_cell:
            cur_cell.make_barrier()

    def right_click_event(self, pos):
        row, col = self.get_clicked_pos(pos)
        if not (1 <= row < (GRID_ROWS - 1) and 1 <= col < (GRID_COLS - 1)):
            return
        cur_cell: GridCell = self.grid[row][col]
        cur_cell.reset()
        if cur_cell == self.start_cell:
            self.start_cell = None
        elif cur_cell == self.end_cell:
            self.end_cell = None

    def fill_neighbours(self):
        for row in self.grid:
            for cell in row:
                cell.update_neighbours(self.grid)

    def reset_grid(self):
        self.start_cell = None
        self.end_cell = None
        self.make_grid()


if len(COLOURS) == 0:
    fill_colours()
