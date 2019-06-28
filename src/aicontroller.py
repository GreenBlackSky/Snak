from basecontroller import BaseController


class AIController(BaseController):
    DIRECTIONS = ((0, -1), (-1, 0), (0, 1), (1, 0))

    def __init__(self):
        BaseController.__init__(self)
        self._step = 0
        self._direction_n = 1

    def decision(self):
        self._step += 1
        if self._step == 5:
            self._desired_direction = AIController.DIRECTIONS[self._direction_n]
            self._direction_n = (self._direction_n + 1) % 4
            self._step = 0
        return BaseController.decision(self)
