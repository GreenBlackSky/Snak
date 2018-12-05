import sys, pygame, time, random


BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
RED = (240, 10, 10)


class Controller:
    def __init__(self):
        self.direction = (0, -1)

    def decision(self):
        ndx, ndy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        cdx, cdy = self.direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self.direction = (ndx, ndy)
        return self.direction

class Snake:
    def __init__(self, pos, mind):
        self.head = pos
        self.tail = pos
        self.cells = [pos]

    def is_selfcrossed(self):
        return (self.head in self.cells[1::])

    def get_tail(self):
        return self.cells[-1]

    def next_pos(self, direction):
        dx, dy = direction
        x, y = self.head
        return (x + dx, y + dy) 

    def move_and_eat(self, pos):
        self.head = pos
        self.cells.insert(0, pos)

    def move(self, pos):
        self.move_and_eat(pos)
        self.tail = self.cells[-1]
        self.cells.pop()


class Game:
    def __init__(self):
        # Config
        self.width, self.height = 80, 45
        self.cell_size = 10
        # Screen
        self.screen = pygame.display.set_mode((self.width*self.cell_size, self.height*self.cell_size))
        self.screen.fill(BLACK)
        # Snake
        self.snake_mind = Controller()
        self.snake = Snake((self.width/2, self.height/2), self.snake_mind)
        self.draw_rect((self.width/2, self.height/2), WHITE)
        # Food
        self.food_pos = self.random_pos()
        self.draw_rect(self.food_pos, RED)
        # Update
        pygame.display.update()

    def random_pos(self):
        return (random.randint(0, self.width), random.randint(0, self.height))

    def draw_rect(self, pos, color):
        x, y = pos
        rect = (x*self.cell_size - self.cell_size/2, \
                y*self.cell_size - self.cell_size/2, \
                self.cell_size, \
                self.cell_size)
        pygame.draw.rect(self.screen, color, rect, 0)

    def get_next_move(self):
        nx, ny = self.snake.next_pos(self.snake_mind.decision())
        if nx < 0: nx = self.width
        elif nx > self.width: nx = 0
        if ny < 0: ny = self.height
        elif ny > self.height: ny = 0
        return (nx, ny)

    def make_move(self, next_pos):
        if self.food_pos == next_pos:
            self.snake.move_and_eat(next_pos)
            self.food_pos = self.random_pos()
            self.draw_rect(self.food_pos, RED)
        else:
            self.snake.move(next_pos)

    def play(self):
        while True:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Move snake
            self.make_move(self.get_next_move())
            # Check for Gameover
            if self.snake.is_selfcrossed():
                sys.exit()
            # Redraw screen
            self.draw_rect(self.snake.head, WHITE)
            self.draw_rect(self.snake.tail, BLACK)
            pygame.display.update()
            time.sleep(0.5)


if __name__ == "__main__":
    pygame.init()
    Game().play()
