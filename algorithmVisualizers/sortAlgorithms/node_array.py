from random import shuffle

from node_elem import NodeElem


class NodeArray:
    def __init__(self, unsorted_array: list):
        self.key_arr = [el for el in unsorted_array]
        self.node_arr = [
            NodeElem(el, pos) for pos, el in enumerate(unsorted_array)
        ]

    def swap(self, a, b):
        self.node_arr[a].update_index(b)
        self.node_arr[b].update_index(a)
        self.node_arr[a], self.node_arr[b] = self.node_arr[b], self.node_arr[a]

    def draw_node(self, win, a):
        self.node_arr[a].draw(win)

    def draw(self, win):
        for el in self.node_arr:
            el.draw(win)

    def reset_node_arr(self):
        self.node_arr = [
            NodeElem(el, pos) for pos, el in enumerate(self.key_arr)
        ]

    def assign_data_set(self, new_array: list):
        self.key_arr = [el for el in new_array]
        self.reset_node_arr()

    def shuffle_array(self, runs):
        for _ in range(runs):
            shuffle(self.key_arr)
        self.reset_node_arr()

    def compare_ab(self, a, b):
        return self.node_arr[a] < self.node_arr[b]
