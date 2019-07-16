"""Module contains AIController class."""

from random import randint, random as randfloat, choice, choices
from basecontroller import BaseController
from config import SCHEME, SCAN_DISTANCE


class AIController(BaseController):
    """
    Neural network-based controller.

    It observes field through `percive`
    and calculates next moving direction in `update`.
    """

    DIRECTIONS = (
        (-1, 0), (0, -1), (1, 0), (0, 1)
    )

    def __init__(self, parent=None, mutation_chance=0):
        """Create new AIController."""
        BaseController.__init__(self)
        self._step = 0
        self._direction_n = 1
        self._nodes_scheme = parent.scheme if parent else SCHEME
        self._neurons = [
            [0] * layer_size
            for layer_size in self._nodes_scheme
        ]
        if parent:
            self._connections = dict(parent._connections)
            mutations_n = randint(
                0,
                int(len(self._connections)*mutation_chance)
            )
            mutations = choices(list(self._connections), k=mutations_n)
            for connection_id in mutations:
                self._connections[connection_id] = randfloat()*choice((1, -1))
        else:
            self._connections = {
                (x2 - 1, y1, x2, y2): randfloat() * choice((1, -1))
                for x2 in range(1, len(self._nodes_scheme))
                for y2 in range(self._nodes_scheme[x2])
                for y1 in range(self._nodes_scheme[x2 - 1])
            }

        self._inputs = [0]*10

    def percive(self, game):
        """
        Percive situation in the game.

        Actualy controller scans 3 directions relative to current direction.
        """
        for i, (dx, dy) in enumerate(self.get_directions()):
            scan_result, distance = AIController._scan_direction(game, dx, dy)
            self._inputs[i*2] = distance
            self._inputs[i*2 + 1] = scan_result

    def update(self):
        """Calculate next moving direction based on input."""
        for i in range(3):
            self._neurons[0][i*2] = self._inputs[i*2] / SCAN_DISTANCE
            self._neurons[0][i*2 + 1] = self._inputs[i*2 + 1] / 4

        number_of_layers = len(self._nodes_scheme)
        for x2 in range(1, number_of_layers):
            x1 = x2 - 1
            for y2 in range(self._nodes_scheme[x2]):
                S = sum(
                    self._neurons[x1][y1]*self._connections[(x1, y1, x2, y2)]
                    for y1 in range(self._nodes_scheme[x1])
                )
                self._neurons[x2][y2] = S if S > 0 else S * 0.01
        self._apply_update_result()

    def _apply_update_result(self):
        left, right = self._neurons[-1]
        if abs(left - right) < 1:
            return
        if left > right:
            self.turn_left()
        elif left < right:
            self.turn_right()

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

    def get_connection(self, x1, y1, x2, y2):
        """Get weight of connection between twoneurons."""
        return self._connections[(x1, y1, x2, y2)]

    def get_input_value(self, n):
        """Get value of input node."""
        return self._inputs[n]

    def get_node_value(self, layer_n, node_n):
        """Pretty much self described."""
        return self._neurons[layer_n][node_n]

    def max_min(self):
        """Get pairs of `(max, min)` values for each layer."""
        return tuple(
            (max(layer), min(layer))
            for layer in self._neurons
        )

    @staticmethod
    def _scan_direction(game, dx, dy):
        x, y = game.snake_head
        distance = 0
        scan_result = 0
        for i in range(1, SCAN_DISTANCE):
            tx, ty = x + dx*i, y + dy*i
            distance += 1
            scan_result = game.scan_cell(tx, ty)
            if scan_result != 0:
                break
        return scan_result, distance

    def reset(self):
        """Reset input values."""
        self._inputs = [0]*10

    @property
    def scheme(self):
        """Get scheme of neural network."""
        return self._nodes_scheme
