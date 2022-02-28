# import math

import heapq

import pygame

NESW = [(-1, 0), (0, -1), (1, 0), (0, 1)]

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
        for r, c in NESW:  # loop north east south west
            new_row, new_col = self.row + r, self.col + c
            if (
                0 <= new_row < GRID_ROWS
                and 0 <= new_col < GRID_COLS
                and not grid[new_row][new_col].is_barrier()
            ):
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

    def right_click_event(self, pos):
        row, col = self.get_clicked_pos(pos)
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


class AStar:
    def __init__(self, vis_tool):
        self.vis_tool = vis_tool

    def huristic(self, node_a, node_b) -> int:
        x1, y1 = node_a
        x2, y2 = node_b
        return abs(x1 - x2) + abs(y1 - y2)

    def construct_path(self, cur_node, parents):
        while cur_node in parents:
            cur_node = parents[cur_node]
            cur_node.make_path()
            self.vis_tool.draw()

    def run_a_star(self):
        start_node = self.vis_tool.start_cell
        end_node = self.vis_tool.end_cell
        self.vis_tool.draw()
        item_number = 0
        in_heap = set()
        priority_queue = []
        parent_map = {}
        distance_g = {
            cell: float("inf") for row in self.vis_tool.grid for cell in row
        }
        distance_f = {
            cell: float("inf") for row in self.vis_tool.grid for cell in row
        }
        distance_g[start_node] = 0
        distance_f[start_node] = self.huristic(
            start_node.get_pos(), end_node.get_pos()
        )
        heapq.heappush(priority_queue, (0, item_number, start_node))
        in_heap.add(start_node)

        while len(in_heap) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            _, _, cur_node = heapq.heappop(priority_queue)
            if cur_node == end_node:
                self.construct_path(cur_node, parent_map)
                end_node.make_end()
                return True

            for neighbour_node in cur_node.neighbours:
                temp_g_score = distance_g[cur_node] + 1
                if temp_g_score < distance_g[neighbour_node]:
                    parent_map[neighbour_node] = cur_node
                    distance_g[neighbour_node] = temp_g_score
                    distance_f[neighbour_node] = temp_g_score + self.huristic(
                        neighbour_node.get_pos(), end_node.get_pos()
                    )
                    if neighbour_node not in in_heap:
                        item_number += 1
                        heapq.heappush(
                            priority_queue,
                            (
                                distance_f[neighbour_node],
                                item_number,
                                neighbour_node,
                            ),
                        )
                        neighbour_node.make_open()
                        in_heap.add(neighbour_node)
            self.vis_tool.draw()
            if cur_node != start_node:
                cur_node.make_closed()
        return False


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
                a_star_vis_tool.right_click_event(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:
                    started = True
                    a_star_vis_tool.fill_neighbours()
                    path_finder = AStar(a_star_vis_tool)
                    path_finder.run_a_star()
                    started = False
                if event.key == pygame.K_SPACE:
                    a_star_vis_tool.reset_grid()
    pygame.quit()


def main():
    fill_colours()
    main_event_loop()


main()
