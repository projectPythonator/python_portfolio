import pygame
from colours import Colour
from node_array import NodeArray


class VisTool:
    def __init__(self, win_width: int, win_height: int, display_name: str):
        self.window = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(display_name)
        self.vis_arr = NodeArray([])

    def assign_data_set(self, unsorted_array: list):
        self.vis_arr.assign_data_set(unsorted_array)

    def reshuffle(self):
        self.vis_arr.shuffle_array(1)

    def update_window(self, a, b):
        self.window.fill(Colour.BLACK)
        self.vis_arr.draw_ith(self.window, a)
        self.vis_arr.draw_ith(self.window, b)
        pygame.display.update()

    def draw(self):
        self.window.fill(Colour.BLACK)
        self.vis_arr.draw(self.window)
        pygame.display.update()
