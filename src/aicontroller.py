"""Module contains the AIController class."""

from random import randint, random as randfloat, choice
from copy import deepcopy
from basecontroller import BaseController
from config import SCHEME, MAX_SCAN_DISTANCE, MUTATION_CHANCE


class AIController(BaseController):
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
        self._step = 0
        self._direction_n = 1
        self._neurons = [
            [0] * layer_size
            for layer_size in SCHEME
        ]
        self._connections = None

        if parent:
            self._inherit_connections(parent)
        else:
            self._generate_connections()

        self._inputs = [0]*3
        self._distances = [0]*3

    def percive(self, game):
        """
        Percive the situation in the game.

        Actualy, the controller scans 3 relative directions.
        """
        for i, (dx, dy) in enumerate(self.get_directions()):
            scan_result, distance = AIController._scan_direction(game, dx, dy)
            self._inputs[i] = scan_result
            self._distances[i] = distance

    def update(self):
        """Calculate the next moving direction based on the input."""
        for i in range(3):
            self._neurons[0][i] = self._inputs[i] - 1

        for i in range(3):
            self._neurons[0][i + 3] = self._distances[i]/MAX_SCAN_DISTANCE

        for layer_n, connections in enumerate(self._connections):
            start_nodes = self._neurons[layer_n]
            end_nodes = self._neurons[layer_n + 1]
            for end_node_n in range(len(end_nodes)):
                weights = connections[end_node_n]
                S = sum(
                    val * weight
                    for val, weight in zip(start_nodes, weights)
                )
                end_nodes[end_node_n] = S if S > 0 else S * 0.01
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

    def get_connection(self, layer_n, start_node_n, end_node_n):
        """Get the weight of connection between twoneurons."""
        return self._connections[layer_n][end_node_n][start_node_n]

    def get_input_value(self, n):
        """Get the value of input node."""
        return self._inputs[n]

    def get_distance_value(self, n):
        """Get distance, on wich relative sensor has been triggered."""
        return self._distances[n]

    def get_node_value(self, layer_n, node_n):
        """Pretty much self described."""
        return self._neurons[layer_n][node_n]

    def max_min(self):
        """Get pairs of `(max, min)` values for each layer."""
        return tuple(
            (max(layer), min(layer))
            for layer in self._neurons
        )

    def reset(self):
        """Reset input values."""
        self._inputs = [0]*3
        self._distances = [0]*3

    def _inherit_connections(self, parent):
        self._connections = deepcopy(parent._connections)
        connections_n = sum(
            SCHEME[i] * SCHEME[i + 1]
            for i in range(len(SCHEME) - 1)
        )
        mutations_n = randint(0, int(connections_n * MUTATION_CHANCE) - 1)

        for _ in range(mutations_n):
            layer_n = randint(0, len(SCHEME) - 2)
            start_node_n = randint(0, SCHEME[layer_n] - 1)
            end_node_n = randint(0, SCHEME[layer_n + 1] - 1)
            val = randfloat() * choice((-1, 1))
            self._connections[layer_n][end_node_n][start_node_n] = val

    def _generate_connections(self):
        self._connections = [
            [
                [
                    randfloat() * choice((-1, 1))
                    for start_node_n in range(SCHEME[layer_n])
                ]
                for end_node_n in range(SCHEME[layer_n + 1])
            ]
            for layer_n in range(len(SCHEME) - 1)
        ]

    def _apply_update_result(self):
        left, right = self._neurons[-1]
        if abs(left - right) < 0.5:
            return
        if left > right:
            self.turn_left()
        elif left < right:
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
