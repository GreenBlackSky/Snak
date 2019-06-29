"""Tetris scene."""


from tkinter import Canvas


class GameScene(Canvas):
    """Visual representation of game.

    Needs GameFrame as master.
    """

    def __init__(self, master, **kargs):
        """Create GameScene."""
        super().__init__(master, **kargs)
        self._width = kargs.get('width', 40)
        self._height = kargs.get('height', 20)
        self._cell_size = kargs.get('cell_size', 10)

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

    def clear(self):
        for item in self.find_all():
            self.itemconfig(item, fill='black')

    def draw(self, game):
        self.clear()
        for x, y in game.snake_body:
            item = self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            )
            self.itemconfig(item, fill='white')

        x, y = game.snake_head
        self.itemconfig(
            self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            ),
            fill='red'
        )

        x, y = game.food_pos
        self.itemconfig(
            self.find_closest(
                (x + 0.5)*self._cell_size,
                (y + 0.5)*self._cell_size
            ),
            fill='green'
        )
