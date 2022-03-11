import pygame
from colour.py import Colour


class NodeCell:
    padding_x = 20
    padding_y = 20

    def __init__(self, cell_height: int, cell_width: int):
        self.height = cell_height
        self.width = cell_width
        self.colour = Colour.WHITE

    def is_observed(self) -> bool:
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
                (NodeCell.padding_x + self.width * pos),
                NodeCell.padding_y,
                self.width,
                self.height,
            ),
        )
