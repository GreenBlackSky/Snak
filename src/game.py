"""Module contains logic for a game of snak."""


from random import randint
from controller import Controller


class Game:
    """Class implements base logic of game."""

    class Snake:
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

    def __init__(self, width, height):
        """Create field for snake with given sizes."""
        self.width, self.height = width, height
        self.snake_mind = Controller()
        self.snake = Game.Snake((self.width/2, self.height/2))
        self.food_pos = self.random_pos()
        self.score = 0

    def random_pos(self):
        """Get some random empty pos on field."""
        ret = self.snake.head
        while ret in self.snake.cells or ret == self.snake.tail:
            ret = (randint(0, self.width - 1), randint(0, self.height - 1))
        return ret

    def get_next_move(self):
        """Get next snake head position."""
        nx, ny = self.snake.next_pos(self.snake_mind.decision())
        if nx < 0:
            nx = self.width
        elif nx >= self.width:
            nx = 0
        if ny < 0:
            ny = self.height
        elif ny >= self.height:
            ny = 0
        return nx, ny

    def make_move(self, next_pos):
        """Update situation on field."""
        if self.food_pos == next_pos:
            self.snake.move_and_eat(next_pos)
            self.food_pos = self.random_pos()
            self.score += 1
        else:
            self.snake.move(next_pos)

# TODO Add some obstacles
