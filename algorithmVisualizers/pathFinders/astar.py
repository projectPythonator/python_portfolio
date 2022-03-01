# import math
import heapq

import pygame
from vis_tool import GRID_HEIGHT, GRID_WIDTH, Visualizer


class AStar:
    def __init__(self, vis_tool):
        self.vis_tool = vis_tool

    def huristic(self, node_a, node_b) -> float:
        x1, y1 = node_a
        x2, y2 = node_b
        return abs(x1 - x2) + abs(y1 - y2)

    def construct_path(self, cur_node, parents):
        while cur_node in parents:
            cur_node = parents[cur_node]
            cur_node.make_path()
            self.vis_tool.draw()
        cur_node.make_start()

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
        heapq.heappush(priority_queue, (0, item_number, 0, start_node))
        in_heap.add(start_node)

        while len(in_heap) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            _, _, g_dist, cur_node = heapq.heappop(priority_queue)
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
                                temp_g_score,
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
    a_star_vis_tool = Visualizer(
        GRID_WIDTH, GRID_HEIGHT, "a* visualization tool"
    )
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
    main_event_loop()


main()
