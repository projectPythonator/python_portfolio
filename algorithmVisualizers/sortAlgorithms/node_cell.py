import pygame
from colour.py import Colour


class NodeCell:
    cell_pad_x = 20
    cell_pad_y = 20
    cell_width = 2

    def __init__(self, cell_height: int):
        self.height = cell_height
        self.colour = Colour.WHITE

    def update_height(self, new_height: int):
        self.height = new_height

    def is_observing(self) -> bool:
        return self.colour == Colour.RED

    def is_unsorted(self) -> bool:
        return self.colour == Colour.WHITE

    def is_sorted(self) -> bool:
        return self.colour == Colour.GREEN

    def is_ordered(self) -> bool:
        return self.colour == Colour.BLUE

    def make_observing(self):
        self.colour = Colour.RED

    def make_unsorted(self):
        self.colour = Colour.WHITE

    def make_sorted(self):
        self.colour = Colour.GREEN

    def make_ordered(self):
        self.colour = Colour.BLUE

    def draw(self, win, pos):
        pygame.draw.rect(
            win,
            self.colour,
            (
                (NodeCell.cell_pad_x + NodeCell.cell_width * pos),
                NodeCell.cell_pad_y,
                NodeCell.cell_width,
                self.height,
            ),
        )
