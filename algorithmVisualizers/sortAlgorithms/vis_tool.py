import pygame
from colours.py import Colour
from node_array.py import NodeArray


class VisTool:
    def __init__(self, win_width: int, win_height: int, display_name: str):
        self.window = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(display_name)
        self.vis_arr = NodeArray([])

    def assign_data_set(self, unsorted_array: list):
        self.vis_arr.assign_data_set(unsorted_array)

    def reshuffle(self):
        self.vis_arr.shuffle_array()

    def draw(self):
        self.window.fill(Colour.BLACK)
        self.vis_arr.draw(self.window)
        pygame.display.update()
