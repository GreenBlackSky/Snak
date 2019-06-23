"""Tetris scene."""


from tkinter import Canvas

from game import Game
from basecontroller import BaseController


class GameScene(Canvas):
    """Visual representation of game.

    Needs GameFrame as master.
    """

    def __init__(self, master, cell_size=10, step=50, **kargs):
        """Create GameScene."""
        super().__init__(master, **kargs)
        self._width = 40
        self._height = 20
        self._cell_size = cell_size
        self._step = step

        self.config(
            width=(self._width*self._cell_size),
            height=(self._height*self._cell_size),
            background='white'
        )

        for y in range(self._height):
            for x in range(self._width):
                self.create_rectangle(
                    x*self._cell_size,
                    y*self._cell_size,
                    x*self._cell_size + self._cell_size,
                    y*self._cell_size + self._cell_size
                )

        self._controller = BaseController()
        self._game = Game(
            self._controller,
            self._width,
            self._height
        )

        self.bind("<Key-Up>", lambda event: self._controller.move_up())
        self.bind("<Key-Down>", lambda event: self._controller.move_down())
        self.bind("<Key-Left>", lambda event: self._controller.move_left())
        self.bind("<Key-Right>", lambda event: self._controller.move_right())
        self._run = False
        self.update()

    def update(self):
        """Update GameScene.

        Schedules call of itself.
        """
        if not self._run:
            self.after(self._step, self.update)
            return

        if self._game.snake_collided():
            self.after(self._step, self.update)
            self.master.master.you_lost()
            return

        self._game.update()
        self.master.score = self._game.score
        self._clear()
        self._draw_filled_cells()

        self.after(self._step, self.update)

    def restart_game(self):
        """Restart game.

        New game is held on pause.
        """
        self._game.restart()
        self._run = False
        self._clear()

    def _clear(self):
        for item in self.find_all():
            self.itemconfig(item, fill='black')

    def _draw_filled_cells(self):
        for x, y in self._game.snake.cells:
            item = self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            )
            self.itemconfig(item, fill='white')

        x, y = self._game.snake.head
        self.itemconfig(
            self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            ),
            fill='red'
        )

        x, y = self._game.food_pos
        self.itemconfig(
            self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            ),
            fill='green'
        )

    @property
    def run(self):
        """Check if game is running.

        If it is not, update method still schedules self-calls,
        but do nothing aside of it.
        """
        return self._run

    @run.setter
    def run(self, value):
        """Make game stop updating itself or run again."""
        self._run = value

# TODO create TkController
# TODO control speed of movement
