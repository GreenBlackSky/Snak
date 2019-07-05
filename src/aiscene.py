from gamescene import GameScene
from config import CELL_SIZE


class AIScene(GameScene):

    def __init__(self, master, controller):
        self._controller = controller
        self._sensor_cells = set()
        self._visible_cells = set()
        GameScene.__init__(self, master)

    def clear(self):
        GameScene.clear(self)
        self._sensor_cells = set()

    def redraw(self, game):
        self._reset_visible_cells()
        self._reset_sensor_cells()
        x, y = game.snake_head
        for i, (dx, dy) in enumerate(self._controller.get_directions()):
            dist = self._controller.get_input_value(i*2)
            val = self._controller.get_input_value(i*2 + 1)
            self._set_visible_cells(x, y, dx, dy, dist)
            self._set_sensor_cell(x + dx*dist, y + dy*dist, val)
        GameScene.redraw(self, game)

    def _reset_sensor_cells(self):
        for item, color in self._sensor_cells:
            self.itemconfig(item, fill=color)
        self._sensor_cells.clear()

    def _reset_visible_cells(self):
        for item in self._visible_cells:
            self.itemconfig(item, fill='black')
        self._visible_cells.clear()

    def _set_sensor_cell(self, x, y, val):
        if val == 3:
            color = 'cyan'
        elif val == 2 or val == 1:
            color = 'magenta'
        else:
            color = 'yellow'
        item = self.find_closest(
            (x + 0.5)*CELL_SIZE,
            (y + 0.5)*CELL_SIZE
        )
        self._sensor_cells.add((item, self.itemcget(item, 'fill')))
        self.itemconfig(item, fill=color)

    def _set_visible_cells(self, x, y, dx, dy, dist):
        for j in range(1, dist):
            cx, cy = x + dx*j, y + dy*j
            item = self.find_closest(
                (cx + 0.5)*CELL_SIZE,
                (cy + 0.5)*CELL_SIZE
            )
            self._visible_cells.add(item)
            self.itemconfig(item, fill='blue')