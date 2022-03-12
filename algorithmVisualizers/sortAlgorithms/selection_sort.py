from time import sleep

import pygame
from colours import Colour
from vis_tool import VisTool


def selection_sort(tool):
    tool.draw()
    data_size = len(tool.vis_arr.node_arr)
    for i in range(data_size - 1):
        min_el = i
        tool.vis_arr.node_arr[i].selected()
        tool.draw()
        for j in range(i + 1, data_size):
            sleep(0.0001)
            tool.vis_arr.node_arr[j].observe()
            tool.update_nodes([j])
            if tool.vis_arr.compare_ab(j, min_el):
                tool.vis_arr.node_arr[min_el].unobserve()
                tool.vis_arr.node_arr[j].selected()
                tool.update_nodes([min_el, j])
                min_el = j
            else:
                tool.vis_arr.node_arr[j].unobserve()
                tool.update_nodes([j])
        tool.vis_arr.swap(i, min_el)
        tool.vis_arr.node_arr[min_el].unobserve()
        tool.vis_arr.node_arr[i].unobserve()
        i += 1
    pygame.quit()


def main():
    print(Colour.BLACK)
    sample_set = [i + 1 for i in range(200)]
    tool = VisTool(1500, 800, "insertion sort")
    tool.assign_data_set(sample_set)
    tool.reshuffle()
    selection_sort(tool)


main()
