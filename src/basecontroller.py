"""Module contains Controller class.

Controller is a bridge between app and game-logic.
"""


class BaseController:
    """Bridge class, allows user to control snake."""

    def __init__(self):
        """Initialize Controller.

        Initial direction is up.
        """
        self.direction = (0, -1)
        self.desired_direction = self.direction

    def move_up(self):
        self.desired_direction = (0, -1)

    def move_down(self):
        self.desired_direction = (0, 1)

    def move_left(self):
        self.desired_direction = (-1, 0)

    def move_right(self):
        self.desired_direction = (1, 0)

    def decision(self):
        """Get next move."""
        ndx, ndy = self.desired_direction
        cdx, cdy = self.direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self.direction = (ndx, ndy)
        return self.direction
