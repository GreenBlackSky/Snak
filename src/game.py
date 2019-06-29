"""Module contains logic for a game of snak."""


from random import randint


class Game:
    """Class implements base logic of game."""

    class _Snake:
        """Abstraction for snake itself."""

        def __init__(self, pos):
            """Create small snake in given pos."""
            self.head = pos
            self.tail = pos
            self.cells = [pos]

        def is_selfcrossed(self):
            """Check if snake has bumped into itself."""
            return self.head in self.cells[1::]

        def next_pos(self, direction):
            """Get position, where snakes head will be on next turn."""
            dx, dy = direction
            x, y = self.head
            return x + dx, y + dy

        def move_and_eat(self, pos):
            """Put head to given coordinates."""
            self.head = pos
            self.cells.insert(0, pos)

        def move(self, pos):
            """Put head to given coordinates and pull tail."""
            self.move_and_eat(pos)
            self.tail = self.cells[-1]
            self.cells.pop()

    def __init__(self, controller, width, height):
        """Create field for snake with given sizes."""
        self._width, self._height = width, height
        self._controller = controller
        self._snake = None
        self._food_pos = None
        self._score = 0
        self.restart()

    def _random_pos(self):
        ret = self._snake.head
        while ret in self._snake.cells or ret == self._snake.tail:
            ret = (randint(0, self._width - 1), randint(0, self._height - 1))
        return ret

    def _get_next_move(self):
        nx, ny = self._snake.next_pos(self._controller.decision())
        if nx < 0:
            nx = self._width
        elif nx >= self._width:
            nx = 0
        if ny < 0:
            ny = self._height
        elif ny >= self._height:
            ny = 0
        return nx, ny

    def update(self):
        """Update situation on field."""
        next_pos = self._get_next_move()
        if self._food_pos == next_pos:
            self._snake.move_and_eat(next_pos)
            self._food_pos = self._random_pos()
            self._score += 1
        else:
            self._snake.move(next_pos)

    def is_lost(self):
        """Check if snake has collided with obstacle."""
        return self._snake.is_selfcrossed()

    def restart(self):
        """Restart game"""
        self._controller.move_up()
        self._snake = Game._Snake((self._width/2, self._height/2))
        self._food_pos = self._random_pos()
        self._score = 0

    @property
    def score(self):
        return self._score

    @property
    def snake_body(self):
        return tuple(self._snake.cells)

    @property
    def snake_head(self):
        return self._snake.head

    @property
    def food_pos(self):
        return self._food_pos
