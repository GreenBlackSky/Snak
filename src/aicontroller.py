"""Module contains the AIController class."""

from numpy import zeros, sign as np_sign
from rnn import RNN
from basecontroller import BaseController
from config import MAX_SCAN_DISTANCE


class AIController(BaseController, RNN):
    """
    Neural network-based controller.

    It observes the field through the `percive` method
    and calculates the next moving direction in the `update` method.
    """

    DIRECTIONS = (
        (-1, 0), (0, -1), (1, 0), (0, 1)
    )

    def __init__(self, parent=None):
        """Create new AIController."""
        BaseController.__init__(self)
        RNN.__init__(self, parent)
        self._step = 0
        self._direction_n = 1

        self._inputs = zeros(3, dtype=int)

    def percive(self, game):
        """
        Percive the situation in the game.

        Actualy, the controller scans 3 relative directions.
        """
        for i, (dx, dy) in enumerate(self.get_directions()):
            scan_result, distance = AIController._scan_direction(game, dx, dy)
            self._inputs[i] = scan_result*distance

    def update(self):
        """Calculate the next moving direction based on the input."""
        for i in range(3):
            self._neurons[0][i] = self._inputs[i] / MAX_SCAN_DISTANCE

        RNN.update(self)

        self._apply_update_result()

    def get_directions(self):
        """Get current scanning directions."""
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        return (
            AIController.DIRECTIONS[i % 4]
            for i in range(
                4 + cur_dir_n - 1,
                4 + cur_dir_n + 2
            )
        )

    def get_input_value(self, n):
        """Get the value of input node."""
        return int(np_sign(self._inputs[n]))

    def get_distance_value(self, n):
        """Get distance, on wich relative sensor has been triggered."""
        return abs(self._inputs[n])

    def reset(self):
        """Reset input values."""
        self._inputs = [0]*3
        self._distances = [0]*3

    def _apply_update_result(self):
        if self._neurons[-1][0] > 0.5:
            self.turn_left()
        elif self._neurons[-1][0] < -0.5:
            self.turn_right()

    @staticmethod
    def _scan_direction(game, dx, dy):
        x, y = game.snake_head
        distance = 0
        scan_result = 0
        for i in range(1, MAX_SCAN_DISTANCE):
            tx, ty = x + dx*i, y + dy*i
            distance += 1
            scan_result = game.scan_cell(tx, ty)
            if scan_result != 0:
                break
        return scan_result, distance
