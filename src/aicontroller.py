from random import random as randfloat, randint
from basecontroller import BaseController


class AIController(BaseController):
    DIRECTIONS = (
        (-1, 0), (-1, -1), (0, -1), (1, -1),
        (1, 0), (1, 1), (0, 1), (-1, 1)
    )
    SCAN_DISTANCE = 5

    class _Neuron(object):
        def __init__(self):
            self._inputs = []
            self._value = 0

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, val):
            self._value = val

        def connect(self, node, weight):
            self._inputs.append((node, weight))

        def activate(self):
            S = sum(
                weight * node.value
                for node, weight in self._inputs
            )
            self._value = S if S > 0 else S * 0.01

    def __init__(self):
        BaseController.__init__(self)
        self._step = 0
        self._direction_n = 1
        self._nodes_scheme = (10, 8, 5, 3)
        self._neurons = [
            [AIController._Neuron() for _ in range(layer_size)]
            for layer_size in self._nodes_scheme
        ]
        for i in range(len(self._nodes_scheme) - 1):
            for node_1 in self._neurons[i + 1]:
                for node_2 in self._neurons[i]:
                    weight = randfloat()
                    sign = 1 if randint(0, 1) == 1 else -1
                    node_1.connect(node_2, weight * sign)

    def update(self):
        for layer_n in range(1, len(self._neurons)):
            for node in self._neurons[layer_n]:
                node.activate()
        self._apply_update_result()

    def percive(self, game):
        masks = self._get_masks()
        for i, mask in enumerate(masks):
            scan_result, distance = AIController._scan_direction(game, mask)
            self._neurons[0][i*2].value = distance/AIController.SCAN_DISTANCE
            self._neurons[0][i*2 + 1].value = scan_result/4

    def _apply_update_result(self):
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        v1, v2, v3 = [self._neurons[-1][i].value for i in range(3)]
        if v1 > max(v2, v3):
            self._direction = AIController.DIRECTIONS[(8 + cur_dir_n - 2) % 8]
        elif v3 > max(v1, v2):
            self._direction = AIController.DIRECTIONS[(8 + cur_dir_n + 2) % 8]

    def _get_masks(self):
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        return (
            AIController.DIRECTIONS[i % 8]
            for i in range(
                8 + cur_dir_n - 2,
                8 + cur_dir_n + 3
            )
        )

    @staticmethod
    def _scan_direction(game, mask):
        x, y = game.snake_head
        dx, dy = mask
        distance = 0
        scan_result = 0
        for _ in range(AIController.SCAN_DISTANCE):
            x, y = x + dx, y + dy
            distance += 1
            scan_result = game.scan_cell(x, y)
            if scan_result != 0:
                break
        return scan_result, distance

    @property
    def scheme(self):
        return self._nodes_scheme
