import unittest

import pygame
from colours import Colour


class HeightNegativeError(Exception):
    """Exception raised when you try to set height < 0.

    Attributes:
        height -- input height which cause error
        message -- expected value and given
    """

    def __init__(self, height, message="cell height must be negative"):
        self.height = height
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{}, height given was: {}".format(self.message, self.height)


class HeightOffScreenError(Exception):
    """Exception raised when you try to height too big.

    Attributes:
        max_height -- max height allowed
        height -- height given
        message -- expected value and given
    """

    def __init__(self, max_height, height, message="height should fit screen"):
        self.height = height
        self.max_height = max_height
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{}, max height is {} given was {}".format(
            self.message, self.max_height, self.height
        )


class NegativeIndexError(Exception):
    """Exception raised when pos is negative.

    Attributes:
        pos -- position give error
        message -- expected value and given
    """

    def __init__(self, pos, message="index needs to be positive"):
        self.pos = pos
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{}, index given was {}".format(self.message, self.pos)


class NodeCell:
    cell_pad_x = 20
    win_height = 800
    cell_width = 2

    def __init__(self, cell_height: int):
        if cell_height < 0:
            raise HeightNegativeError(cell_height)
        if cell_height > NodeCell.win_height:
            raise HeightOffScreenError
        self.height = cell_height
        self.colour = Colour.WHITE

    def is_observing(self) -> bool:
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

    def draw_bar(self, win, colour, x_pos, y_pos, x_len, y_len):
        pygame.draw.rect(
            win,
            colour,
            (x_pos, y_pos, x_len, y_len),
        )

    def draw(self, win, pos):
        self.draw_bar(
            win,
            Colour.BLACK,
            NodeCell.cell_pad_x + NodeCell.cell_width * pos,
            0,
            NodeCell.cell_width,
            NodeCell.win_height - self.height,
        )
        self.draw_bar(
            win,
            self.colour,
            NodeCell.cell_pad_x + NodeCell.cell_width * pos,
            NodeCell.win_height - self.height,
            NodeCell.cell_width,
            self.height,
        )


class NodeCellInitTest(unittest.TestCase):
    def test_invalid_height_1(self):
        height_value = -1
        with self.assertRaises(Exception) as cm:
            self.node_cell = NodeCell(height_value)
        nche_exception = cm.exception
        self.assertEqual(nche_exception.height, height_value)

    def test_invalid_height_2(self):
        height_value = -1000000
        with self.assertRaises(Exception) as cm:
            self.node_cell = NodeCell(height_value)
        nche_exception = cm.exception
        self.assertEqual(nche_exception.height, height_value)

    def test_valid_height_positive_1(self):
        node_cell = NodeCell(1)
        self.assertEqual(1, node_cell.height)
        self.assertEqual(Colour.WHITE, node_cell.colour)


if __name__ == "__main__":
    unittest.main()
