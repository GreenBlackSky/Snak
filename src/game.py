import random
from controller import Controller

class Game:
    class Snake:
        def __init__(self, pos):
            self.head = pos
            self.tail = pos
            self.cells = [pos]

        def is_selfcrossed(self):
            return self.head in self.cells[1::]

        def next_pos(self, direction):
            dx, dy = direction
            x, y = self.head
            return x + dx, y + dy

        def move_and_eat(self, pos):
            self.head = pos
            self.cells.insert(0, pos)

        def move(self, pos):
            self.move_and_eat(pos)
            self.tail = self.cells[-1]
            self.cells.pop()

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.snake_mind = Controller()
        self.snake = Game.Snake((self.width/2, self.height/2))
        self.food_pos = self.random_pos()
        self.score = 0

    def random_pos(self):
        ret = self.snake.head
        while ret in self.snake.cells or ret == self.snake.tail:
            ret = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return ret

    def get_next_move(self):
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
        if self.food_pos == next_pos:
            self.snake.move_and_eat(next_pos)
            self.food_pos = self.random_pos()
            self.score += 1
        else:
            self.snake.move(next_pos)
