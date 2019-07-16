"""Module contains logic for a game of snak."""


from random import randint, choice, sample
from config import WIDTH, HEIGHT, RELATIVE_OBSTACLE_N, OBSTACLE_RATE


class Game:
    """Class implements the base logic of the game."""

    class _Snake:
        """Abstraction for the snake itself."""

        def __init__(self, pos):
            """Create the small snake in the given pos."""
            self.head = pos
            self.tail = pos
            self.cells = [pos]

        def is_selfcrossed(self):
            """Check if the snake has bumped into itself."""
            return self.head in self.cells[1::]

        def next_pos(self, direction):
            """Get the position of the snakes head by the next turn."""
            dx, dy = direction
            x, y = self.head
            return x + dx, y + dy

        def move_and_eat(self, pos):
            """Place the head to the given coordinates."""
            self.head = pos
            self.cells.insert(0, pos)

        def move(self, pos):
            """Place the head to the given coordinates and pull the tail."""
            self.move_and_eat(pos)
            self.tail = self.cells[-1]
            self.cells.pop()

    def __init__(self):
        """Create the field for the snake with given sizes."""
        self._snake = None
        self._food_pos = None
        self._obstacles = None
        self._score = 0
        self._is_lost = False
        self.restart()

    def restart(self):
        """Restart the game."""
        self._generate_obstacles()
        self._snake = Game._Snake((WIDTH/2, HEIGHT/2))
        self._food_pos = self._random_pos()
        self._score = 0
        self._is_lost = False

    def update(self, direction):
        """Update the situation on the field."""
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

    @property
    def is_lost(self):
        """Check if the game is lost."""
        return self._is_lost

    @property
    def score(self):
        """Get the current game score."""
        return self._score

    @property
    def snake_head(self):
        """Position of the snakes head."""
        return self._snake.head

    @property
    def snake_neck(self):
        """
        Position of the snakes neck.

        One block behind the head.
        """
        if len(self._snake.cells) > 1:
            ret = self._snake.cells[1]
        else:
            ret = self._snake.head
        return ret

    @property
    def snake_body(self):
        """Get positions of blocks in the snakes body."""
        return tuple(self._snake.cells)

    @property
    def snake_tail(self):
        """Get the position of the snakes tail."""
        return self._snake.tail

    @property
    def food_pos(self):
        """Get the position of the food."""
        return self._food_pos

    @property
    def obstacles(self):
        """Get the list of all occupied cells."""
        return list(self._obstacles)

    def scan_cell(self, x, y):
        """Check what is insede the cell on the given coordinates."""
        pos = ((x + WIDTH) % WIDTH, (y + HEIGHT) % HEIGHT)
        if pos == self._food_pos:
            return 2
        elif pos in self._obstacles or \
            pos in self._snake.cells \
                or pos == self._snake.tail:
            return 1
        else:
            return 0
