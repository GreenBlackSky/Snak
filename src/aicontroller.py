from random import random as randfloat, randint
from basecontroller import BaseController


class AIController(BaseController):
    DIRECTIONS = (
        (-1, 0), (-1, -1), (0, -1), (1, -1),
        (1, 0), (1, 1), (0, 1), (-1, 1)
    )
    SCAN_DISTANCE = 10

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
        self._inputs = [0]*10

    def update(self):
        for i in range(5):
            self._neurons[0][i*2].value = self._inputs[i*2]
            self._neurons[0][i*2 + 1].value = self._inputs[i*2 + 1]
        self._scale_layer_output(0)

        for layer_n in range(1, len(self._neurons)):
            for node in self._neurons[layer_n]:
                node.activate()
            self._scale_layer_output(layer_n)
        self._apply_update_result()

    def percive(self, game):
        for i, (dx, dy) in enumerate(self.get_directions()):
            scan_result, distance = AIController._scan_direction(game, dx, dy)
            self._inputs[i*2] = distance
            self._inputs[i*2 + 1] = scan_result

    def _apply_update_result(self):
        cur_dir_n = AIController.DIRECTIONS.index(self._direction)
        v1, v2, v3 = [self._neurons[-1][i].value for i in range(3)]
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

    def get_input_value(self, n):
        return self._inputs[n]

    def _scale_layer_output(self, layer_n):
        layer = self._neurons[layer_n]
        mean = sum(neuron.value for neuron in layer)/len(layer)
        std = (
            sum(
                (neuron.value - mean)**2
                for neuron in layer
            )/(len(layer) - 1)
        )**0.5
        for neuron in layer:
            neuron.value = (neuron.value - mean)/std

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

    @property
    def scheme(self):
        return self._nodes_scheme
