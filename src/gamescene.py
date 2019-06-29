"""Tetris scene."""


from tkinter import Canvas
from config import WIDTH, CELL_SIZE, HEIGHT


class GameScene(Canvas):
    """Visual representation of game.

    Needs GameFrame as master.
    """

    def __init__(self, master, **kargs):
        """Create GameScene."""
        super().__init__(master, **kargs)

        self.config(
            width=(WIDTH*CELL_SIZE),
            height=(HEIGHT*CELL_SIZE),
            background='white'
        )

        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.create_rectangle(
                    x*CELL_SIZE,
                    y*CELL_SIZE,
                    x*CELL_SIZE + CELL_SIZE,
                    y*CELL_SIZE + CELL_SIZE
                )

    def clear(self):
        for item in self.find_all():
            self.itemconfig(item, fill='black')

    def draw(self, game):
        self.clear()
        for x, y in game.obstacles:
            self._fill_cell(x, y, 'gray')
        for x, y in game.snake_body:
            self._fill_cell(x, y, 'white')
        self._fill_cell(*game.snake_head, 'red')
        self._fill_cell(*game.food_pos, 'green')

    def redraw(self, game):
        self._fill_cell(*game.snake_neck, 'white')
        self._fill_cell(*game.snake_head, 'red')
        self._fill_cell(*game.snake_tail, 'black')
        self._fill_cell(*game.food_pos, 'green')

    def _fill_cell(self, x, y, color):
        self.itemconfig(
            self.find_closest(
                (x + 0.5)*CELL_SIZE,
                (y + 0.5)*CELL_SIZE
            ),
            fill=color
        )
