"""Module contains BaseController class.

Controller is a bridge between app and game-logic.
"""


class BaseController:
    """Bridge class, allows user to control snake."""

    DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def __init__(self):
        """Initialize Controller.

        Initial direction is up.
        """
        self._direction = (0, -1)
        self._desired_direction = self._direction

    def move_up(self):
        """Set moving direction to absulute up."""
        self._desired_direction = (0, -1)

    def move_down(self):
        """Set moving direction to absulute down."""
        self._desired_direction = (0, 1)

    def move_left(self):
        """Set moving direction to absulute left."""
        self._desired_direction = (-1, 0)

    def move_right(self):
        """Set moving direction to absulute right."""
        self._desired_direction = (1, 0)

    def turn_left(self):
        """Set moving direction to relative left."""
        cur_dir_n = BaseController.DIRECTIONS.index(self._direction)
        self._direction = BaseController.DIRECTIONS[(cur_dir_n + 1) % 4]

    def turn_right(self):
        """Set moving direction to relative right."""
        cur_dir_n = BaseController.DIRECTIONS.index(self._direction)
        self._direction = BaseController.DIRECTIONS[(cur_dir_n + 3) % 4]

    def update(self):
        """Update current moving direction due to controller input."""
        ndx, ndy = self._desired_direction
        cdx, cdy = self._direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self._direction = (ndx, ndy)

    @property
    def direction(self):
        """Get current moving direction."""
        return self._direction
