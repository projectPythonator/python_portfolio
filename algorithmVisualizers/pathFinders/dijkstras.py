# import math
import heapq

import pygame
from vis_tool import GRID_HEIGHT, GRID_WIDTH, Visualizer


class Dijkstras:
    def __init__(self, vis_tool):
        self.vis_tool = vis_tool

    def construct_path(self, cur_node, parents):
        while cur_node in parents:
            cur_node = parents[cur_node]
            cur_node.make_path()
            self.vis_tool.draw()
        cur_node.make_start()

    def run_dijkstras(self):
        start_node = self.vis_tool.start_cell
        end_node = self.vis_tool.end_cell
        self.vis_tool.draw()
        priority_queue = []
        parent_map = {}
        distance_g = {
            cell: 2**64 for row in self.vis_tool.grid for cell in row
        }
        distance_g[start_node] = 0
        heapq.heappush(priority_queue, (0, start_node))

        while len(priority_queue) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            g_dist, cur_node = heapq.heappop(priority_queue)
            if cur_node == end_node:
                self.construct_path(cur_node, parent_map)
                end_node.make_end()
                return True
            if distance_g[cur_node] < g_dist:
                continue
            for neighbour_node in cur_node.neighbours:
                temp_g_score = distance_g[cur_node] + 1
                if temp_g_score < distance_g[neighbour_node]:
                    parent_map[neighbour_node] = cur_node
                    distance_g[neighbour_node] = temp_g_score
                    heapq.heappush(
                        priority_queue,
                        (
                            temp_g_score,
                            neighbour_node,
                        ),
                    )
                    neighbour_node.make_open()
            self.vis_tool.draw()
            if cur_node != start_node:
                cur_node.make_closed()
        return False


def main_event_loop():
    dijkstras_vis_tool = Visualizer(
        GRID_WIDTH, GRID_HEIGHT, "a* visualization tool"
    )
    dijkstras_vis_tool.make_grid()
    run = True
    started = False
    while run:
        dijkstras_vis_tool.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:  # left
                dijkstras_vis_tool.left_click_event(pygame.mouse.get_pos())
            elif pygame.mouse.get_pressed()[2]:  # right
                dijkstras_vis_tool.right_click_event(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:
                    started = True
                    dijkstras_vis_tool.fill_neighbours()
                    path_finder = Dijkstras(dijkstras_vis_tool)
                    path_finder.run_dijkstras()
                    started = False
                if event.key == pygame.K_SPACE:
                    dijkstras_vis_tool.reset_grid()
    pygame.quit()


def main():
    main_event_loop()


main()
