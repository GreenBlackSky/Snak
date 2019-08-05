"""Module contains the AIScene widget."""

from gamescene import GameScene


class AIScene(GameScene):
    """
    Scene to display the ai that plays snake.

    Beside game objects, it displays ai sensors.
    """

    def __init__(self, master):
        """Create the AIScene."""
        self._sensor_cells = set()
        self._visible_cells = set()
        super().__init__(master)

    def clear(self):
        """Clear the scene."""
        self._sensor_cells.clear()
        self._visible_cells.clear()
        super().clear()

    def redraw(self, game, controller):
        """
        Update the display.

        It is assumed that the same game has been displayed.
        Only sensors, the game and the food are updated.
        """
        self._reset_visible_cells()
        self._reset_sensor_cells()
        super().redraw(game)
        x, y = game.snake_head
        for i, (dx, dy) in enumerate(controller.get_directions()):
            dist = controller.get_distance_value(i)
            val = controller.get_input_value(i)
            self._set_visible_cells(x, y, dx, dy, dist)
            self._set_sensor_cell(x + dx*dist, y + dy*dist, val)

    def _reset_sensor_cells(self):
        for item, color in self._sensor_cells:
            self.itemconfig(item, fill=color)
        self._sensor_cells.clear()

    def _reset_visible_cells(self):
        for item in self._visible_cells:
            self.itemconfig(item, fill='black')
        self._visible_cells.clear()

    def _set_sensor_cell(self, x, y, val):
        color = {0: 'blue', -1: 'yellow', 1: 'cyan'}[val]
        item, original_color = self._fill_cell(x, y, color)
        self._sensor_cells.add((item, original_color))

    def _set_visible_cells(self, x, y, dx, dy, dist):
        for j in range(1, dist):
            cx, cy = x + dx*j, y + dy*j
            item, original_color = self._fill_cell(cx, cy, 'blue')
            self._visible_cells.add(item)
