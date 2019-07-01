"""Module contains Controller class.

Controller is a bridge between app and game-logic.
"""


class BaseController:
    """Bridge class, allows user to control snake."""

    def __init__(self):
        """Initialize Controller.

        Initial direction is up.
        """
        self._direction = (0, -1)
        self._desired_direction = self._direction

    def move_up(self):
        self._desired_direction = (0, -1)

    def move_down(self):
        self._desired_direction = (0, 1)

    def move_left(self):
        self._desired_direction = (-1, 0)

    def move_right(self):
        self._desired_direction = (1, 0)

    def update(self):
        ndx, ndy = self._desired_direction
        cdx, cdy = self._direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self._direction = (ndx, ndy)

    @property
    def direction(self):
        return self._direction
