# import heapq
# import math

import pygame

GRID_ROWS: int = 50
GRID_COLS: int = 50
GRID_WIDTH: int = 800
GRID_HEIGHT: int = 800
CELL_WIDTH: int = GRID_WIDTH // GRID_COLS
CELL_HEIGHT: int = GRID_HEIGHT // GRID_ROWS

TITLE: str = "A* path finder algorithm"

COLOURS: dict = {}
START_CODE: int = 0
END_CODE: int = 0


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
        self.row = row
        self.col = col
        self.cell_x: int = col * CELL_WIDTH
        self.cell_y: int = row * CELL_HEIGHT
        self.cell_colour = COLOURS["WHITE"]
        self.cell_neighbours = []

    def get_row_col_pos(self):
        return self.row, self.col

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
        pass

    def __lt__(self, other):
        return False


class Visualizer:
    def __init__(self, width: int, height: int, display_name: str):
        self.WINDOW = pygame.display.set_mode((width, height))
        pygame.display.set_caption(display_name)
        self.grid = [[] for i in range(GRID_ROWS)]
        self.start_cell = None
        self.end_cell = None

    def make_grid(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell = GridCell(row, col)
                self.grid[row].append(cell)

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


class AStar:
    def __init__(self):
        pass

    def huristic(self, node_a, node_b) -> int:
        x1, y1 = node_a
        x2, y2 = node_b
        return abs(x1 - x2) + abs(y1 - y2)


def main_event_loop():
    a_star_vis_tool = Visualizer(GRID_WIDTH, GRID_HEIGHT, TITLE)
    a_star_vis_tool.make_grid()
    run = True
    started = False
    while run:
        a_star_vis_tool.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:  # left
                a_star_vis_tool.left_click_event(pygame.mouse.get_pos())

            elif pygame.mouse.get_pressed()[2]:  # right
                pass

    pygame.quit()


def main():
    fill_colours()
    main_event_loop()


main()
