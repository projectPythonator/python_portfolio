from functools import total_ordering

from node_cell import NodeCell


@total_ordering
class NodeElem:
    def __init__(self, value: int, position: int):
        self.key = value
        self.index = position
        self.cell = NodeCell(self.key)

    def __eq__(self, other):
        return (self.key, self.index) == (other.key, other.index)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.key, self.index) < (other.key, other.index)

    def draw(self, win):
        self.cell.draw(win, self.index)

    def observe(self):
        self.cell.make_observing()

    def unobserve(self):
        self.cell.make_unsorted()

    def selected(self):
        self.cell.make_sorted()

    def update_index(self, new_pos):
        self.index = new_pos
