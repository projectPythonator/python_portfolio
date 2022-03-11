import pygame
from colours import Colour
from vis_tool import VisTool


def insertion_sort(tool):
    tool.draw()
    i = 1
    while True:
        if i == len(tool.vis_arr.key_arr):
            break
        tool.vis_arr.node_arr[i].observe()
        tool.draw()
        j = i
        while j > 0 and tool.vis_arr.compare_ab(j, j - 1):
            tool.draw()
            tool.vis_arr.swap(j, j - 1)

            j -= 1
        tool.vis_arr.node_arr[j].unobserve()
        i += 1
    pygame.quit()


def main():
    print(Colour.BLACK)
    sample_set = [i + 1 for i in range(500)]
    tool = VisTool(1500, 800, "insertion sort")
    tool.assign_data_set(sample_set)
    tool.reshuffle()
    insertion_sort(tool)


main()
