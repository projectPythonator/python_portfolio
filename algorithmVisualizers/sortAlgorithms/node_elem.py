from functools import total_ordering

from node_cell.py import NodeCell


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
        self.cell.draw(win, self.key)

    def observe(self):
        self.cell.make_observing()

    def update_key(self, new_key):
        self.key = new_key
        self.cell.update_height(self.key)
