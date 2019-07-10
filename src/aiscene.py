"""Module contains AIScene widget."""

from gamescene import GameScene


class AIScene(GameScene):
    """
    Scene to display ai, playing snake.

    Beside game objects, displays ai sensors.
    """

    def __init__(self, master, controller):
        """Create AIScene."""
        self._controller = controller
        self._sensor_cells = set()
        self._visible_cells = set()
        super().__init__(master)

    def clear(self):
        """Clear scene."""
        self._sensor_cells.clear()
        self._visible_cells.clear()
        super().clear()

    def redraw(self, game):
        """
        Update display.

        It is assumed that the same game has been displayed.
        Only sensors, game and food are updated.
        """
        self._reset_visible_cells()
        self._reset_sensor_cells()
        x, y = game.snake_head
        for i, (dx, dy) in enumerate(self._controller.get_directions()):
            dist = self._controller.get_input_value(i*2)
            val = self._controller.get_input_value(i*2 + 1)
            self._set_visible_cells(x, y, dx, dy, dist)
            self._set_sensor_cell(x + dx*dist, y + dy*dist, val)
        super().redraw(game)

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
            color = 'yellow'
        else:
            color = 'blue'
        item, original_color = self._fill_cell(x, y, color)
        self._sensor_cells.add((item, original_color))

    def _set_visible_cells(self, x, y, dx, dy, dist):
        for j in range(1, dist):
            cx, cy = x + dx*j, y + dy*j
            item, original_color = self._fill_cell(cx, cy, 'blue')
            self._visible_cells.add(item)
