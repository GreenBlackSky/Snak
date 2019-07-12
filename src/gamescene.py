"""Tetris scene."""


from resiziblecanvas import ResizibleCanvas
from config import WIDTH, CELL_SIZE, HEIGHT


class GameScene(ResizibleCanvas):
    """Visual representation of game."""

    def __init__(self, master):
        """Create GameScene."""
        self._cell_w = CELL_SIZE
        self._cell_h = CELL_SIZE
        ResizibleCanvas.__init__(
            self,
            master,
            width=(WIDTH*self._cell_w),
            height=(HEIGHT*self._cell_h)
        )

        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.create_rectangle(
                    x*self._cell_w,
                    y*self._cell_h,
                    (x + 1)*self._cell_w,
                    (y + 1)*self._cell_h
                )

    def _on_resize(self, event):
        self._cell_w *= event.width/self._width
        self._cell_h *= event.height/self._height
        ResizibleCanvas._on_resize(self, event)

    def clear(self):
        """Clear scene."""
        for item in self.find_all():
            self.itemconfig(item, fill='black')

    def draw(self, game):
        """Draw given game."""
        self.clear()
        for x, y in game.obstacles:
            self._fill_cell(x, y, 'gray')
        for x, y in game.snake_body:
            self._fill_cell(x, y, 'white')
        self._fill_cell(*game.snake_head, 'red')
        self._fill_cell(*game.food_pos, 'green')

    def redraw(self, game):
        """
        Update game.

        It is assumed that given game is already being displayed.
        Only head, neck and tail of snake and food are redrawn.
        All obstacles stays the same.
        """
        self._fill_cell(*game.snake_neck, 'white')
        self._fill_cell(*game.snake_head, 'red')
        self._fill_cell(*game.snake_tail, 'black')
        self._fill_cell(*game.food_pos, 'green')

    def _fill_cell(self, x, y, color):
        x = (x + WIDTH) % WIDTH
        y = (y + HEIGHT) % HEIGHT
        item = self.find_closest(
            (x + 0.5)*self._cell_w,
            (y + 0.5)*self._cell_h
        )
        original_color = self.itemcget(item, 'fill')
        self.itemconfig(item, fill=color)
        return item, original_color
