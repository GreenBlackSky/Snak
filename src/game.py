"""Module contains logic for a game of snak."""


from random import randint, choice, sample
from config import WIDTH, HEIGHT, RELATIVE_OBSTACLE_N, OBSTACLE_RATE


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

    def __init__(self):
        """Create field for snake with given sizes."""
        self._snake = None
        self._food_pos = None
        self._obstacles = None
        self._score = 0
        self._is_lost = False
        self.restart()

    def update(self, direction):
        """Update situation on field."""
        next_pos = self._get_next_move(direction)
        if self._is_lost or \
            next_pos in self._obstacles or \
                next_pos in self._snake.cells:
            self._is_lost = True
        elif self._food_pos == next_pos:
            self._snake.move_and_eat(next_pos)
            self._food_pos = self._random_pos()
            self._score += 1
        else:
            self._snake.move(next_pos)

    @property
    def is_lost(self):
        return self._is_lost

    def restart(self):
        """Restart game"""
        self._generate_obstacles()
        self._snake = Game._Snake((WIDTH/2, HEIGHT/2))
        self._food_pos = self._random_pos()
        self._score = 0
        self._is_lost = False

    @property
    def score(self):
        return self._score

    @property
    def snake_head(self):
        return self._snake.head

    @property
    def snake_neck(self):
        if len(self._snake.cells) > 1:
            ret = self._snake.cells[1]
        else:
            ret = self._snake.head
        return ret

    @property
    def snake_body(self):
        return tuple(self._snake.cells)

    @property
    def snake_tail(self):
        return self._snake.tail

    @property
    def food_pos(self):
        return self._food_pos

    @property
    def obstacles(self):
        return list(self._obstacles)

    def scan_cell(self, x, y):
        pos = (x % WIDTH, y % HEIGHT)
        if pos == self._food_pos:
            return 3
        if pos in self._obstacles:
            return 2
        if pos in self._snake.cells or pos == self._snake.tail:
            return 1
        return 0

    def _random_pos(self):
        ret = self._snake.head
        while ret in self._snake.cells or \
            ret == self._snake.tail or \
                ret in self._obstacles:
            ret = (randint(0, WIDTH - 1), randint(0, HEIGHT - 1))
        return ret

    def _get_next_move(self, direction):
        nx, ny = self._snake.next_pos(direction)
        if nx < 0:
            nx = WIDTH
        elif nx >= WIDTH:
            nx = 0
        if ny < 0:
            ny = HEIGHT
        elif ny >= HEIGHT:
            ny = 0
        return nx, ny

    def _generate_obstacles(self):
        self._obstacles = set()
        S = WIDTH * HEIGHT
        obst_N = int(S * RELATIVE_OBSTACLE_N)
        obst_N_full = int(S * OBSTACLE_RATE)

        while len(self._obstacles) < obst_N:
            self._obstacles.add((
                randint(0, WIDTH - 1),
                randint(0, HEIGHT - 1)
            ))

        while len(self._obstacles) < obst_N_full:
            x, y = sample(self._obstacles, 1)[0]
            neighbs = [
                ((nx + WIDTH) % WIDTH, (ny + HEIGHT) % HEIGHT)
                for nx, ny in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
                if (nx, ny) not in self._obstacles
            ]
            if neighbs:
                self._obstacles.add(choice(neighbs))
