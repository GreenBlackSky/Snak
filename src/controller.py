"""Module contains Controller class.

Controller is a bridge between app and game-logic.
"""


class Controller:
    """Bridge class, allows user to control snake."""

    def __init__(self):
        """Initialize Controller.

        Initial direction is up.
        """
        self.direction = (0, -1)
        self.desired_direction = self.direction

    def desire(self, direction):
        """Set next move."""
        self.desired_direction = direction

    def decision(self):
        """Get next move."""
        ndx, ndy = self.desired_direction
        cdx, cdy = self.direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self.direction = (ndx, ndy)
        return self.direction
