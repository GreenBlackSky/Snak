from gamescene import GameScene
from config import CELL_SIZE


class AIScene(GameScene):

    def __init__(self, master, controller):
        self._controller = controller
        self._sensor_cells = set()
        GameScene.__init__(self, master)

    def redraw(self, game):
        GameScene.redraw(self, game)

        for item, color in self._sensor_cells:
            self.itemconfig(item, fill=color)
        self._sensor_cells.clear()

        x, y = game.snake_head
        for i, (dx, dy) in enumerate(self._controller.get_directions()):
            dist = self._controller.get_input_value(i*2)
            val = self._controller.get_input_value(i*2 + 1)
            cx, cy = x + dx*dist, y + dy*dist
            if val == 3:
                color = 'cyan'
            elif val == 2 or val == 1:
                color = 'magenta'
            else:
                color = 'yellow'
            item = self.find_closest(
                (cx + 0.5)*CELL_SIZE,
                (cy + 0.5)*CELL_SIZE
            )
            self._sensor_cells.add((item, self.itemcget(item, 'fill')))
            self.itemconfig(item, fill=color)
