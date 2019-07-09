from random import random as randfloat, randint, choice
from basecontroller import BaseController


class AIController(BaseController):
    DIRECTIONS = (
        (-1, 0), (-1, -1), (0, -1), (1, -1),
        (1, 0), (1, 1), (0, 1), (-1, 1)
    )
    SCAN_DISTANCE = 10

    def __init__(self):
        BaseController.__init__(self)
        self._step = 0
        self._direction_n = 1
        self._nodes_scheme = (10, 8, 5, 3)
        self._neurons = [
            [0] * layer_size
            for layer_size in self._nodes_scheme
        ]
        self._connections = {
            (x2 - 1, y1, x2, y2): randfloat() * choice((1, -1))
            for x2 in range(1, len(self._nodes_scheme))
            for y2 in range(self._nodes_scheme[x2])
            for y1 in range(self._nodes_scheme[x2 - 1])
        }

        self._inputs = [0]*10

    def update(self):
        for i in range(5):
            self._neurons[0][i*2] = self._inputs[i*2] / 5
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

    def percive(self, game):
        for i, (dx, dy) in enumerate(self.get_directions()):
            scan_result, distance = AIController._scan_direction(game, dx, dy)
            self._inputs[i*2] = distance
            self._inputs[i*2 + 1] = scan_result

    def _apply_update_result(self):
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        v1, v2, v3 = [self._neurons[-1][i] for i in range(3)]
        if v1 > max(v2, v3):
            self._direction = AIController.DIRECTIONS[(8 + cur_dir_n - 2) % 8]
        elif v3 > max(v1, v2):
            self._direction = AIController.DIRECTIONS[(8 + cur_dir_n + 2) % 8]

    def get_directions(self):
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        return (
            AIController.DIRECTIONS[i % 8]
            for i in range(
                8 + cur_dir_n - 2,
                8 + cur_dir_n + 3
            )
        )

    def get_connection(self, x1, y1, x2, y2):
        return self._connections[(x1, y1, x2, y2)]

    def get_input_value(self, n):
        return self._inputs[n]

    def get_node_value(self, layer_n, node_n):
        return self._neurons[layer_n][node_n]

    def max_min(self):
        return tuple(
            (max(layer), min(layer))
            for layer in self._neurons
        )

    @staticmethod
    def _scan_direction(game, dx, dy):
        x, y = game.snake_head
        distance = 0
        scan_result = 0
        for i in range(1, AIController.SCAN_DISTANCE):
            tx, ty = x + dx*i, y + dy*i
            distance += 1
            scan_result = game.scan_cell(tx, ty)
            if scan_result != 0:
                break
        return scan_result, distance

    def reset(self):
        self._inputs = [0]*10

    @property
    def scheme(self):
        return self._nodes_scheme
