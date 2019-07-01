from random import random as randfloat
from basecontroller import BaseController


class AIController(BaseController):
    DIRECTIONS = ((0, -1), (-1, 0), (0, 1), (1, 0))

    def __init__(self):
        BaseController.__init__(self)
        self._step = 0
        self._direction_n = 1
        nodes_scheme = [7, 6, 5, 4]
        self._neurons = [
            [0] * size
            for size in nodes_scheme
        ]
        self._connections = [
            [
                [randfloat() for _ in range(nodes_scheme[i + 1])]
                for _ in range(nodes_scheme[i])
            ]
            for i in range(len(nodes_scheme) - 1)
        ]

    def update(self):
        self._step += 1
        if self._step == 5:
            self._desired_direction = AIController.DIRECTIONS[self._direction_n]
            self._direction_n = (self._direction_n + 1) % 4
            self._step = 0
        BaseController.update(self)

    def percive(self, game):
        pass
