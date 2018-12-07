import sys, pygame, time, random


BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
RED = (240, 10, 10)

KEYS = {pygame.K_UP: (0, -1), \
        pygame.K_DOWN: (0, 1), \
        pygame.K_LEFT: (-1, 0), \
        pygame.K_RIGHT: (1, 0)}


class Controller:
    def __init__(self):
        self.direction = (0, -1)
        self.desired_direction = self.direction
        
    def desire(self, direction):
        self.desired_direction = direction
        
    def decision(self):
        ndx, ndy = self.desired_direction
        cdx, cdy = self.direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self.direction = (ndx, ndy)
        return self.direction


class Game:
    class Snake:
        def __init__(self, pos):
            self.head = pos
            self.tail = pos
            self.cells = [pos]

        def is_selfcrossed(self):
            return (self.head in self.cells[1::])

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

    def __init__(self, width, height):
        # Config
        self.width, self.height = width, height
        self.cell_size = 10
        self.fps = 8
        # Screen
        self.screen = pygame.display.set_mode((self.width*self.cell_size, self.height*self.cell_size))
        self.screen.fill(BLACK)
        # Snake
        self.snake_mind = Controller()
        self.snake = Game.Snake((self.width/2, self.height/2))
        self.draw_rect((self.width/2, self.height/2), WHITE)
        # Food
        self.food_pos = self.random_pos()
        self.draw_rect(self.food_pos, RED)
        # Update
        pygame.display.update()

    def random_pos(self):
        ret = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while ret in self.snake.cells:
            ret = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return ret

    def draw_rect(self, pos, color):
        x, y = pos
        rect = (x*self.cell_size, \
                y*self.cell_size, \
                self.cell_size, \
                self.cell_size)
        pygame.draw.rect(self.screen, color, rect, 0)

    def get_next_move(self):
        nx, ny = self.snake.next_pos(self.snake_mind.decision())
        if nx < 0: nx = self.width
        elif nx >= self.width: nx = 0
        if ny < 0: ny = self.height
        elif ny >= self.height: ny = 0
        return (nx, ny)

    def make_move(self, next_pos):
        ret = False
        if self.food_pos == next_pos:
            self.snake.move_and_eat(next_pos)
            ret = True
        else:
            self.snake.move(next_pos)
        return ret

    def play(self):
        while True:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key in KEYS:
                    self.snake_mind.desire(KEYS[event.key])
            # Move snake
            if self.make_move(self.get_next_move()):
                self.food_pos = self.random_pos()
                self.draw_rect(self.food_pos, RED)
            # Check for Gameover
            if self.snake.is_selfcrossed():
                sys.exit()
            # Redraw screen
            self.draw_rect(self.snake.head, WHITE)
            self.draw_rect(self.snake.tail, BLACK)
            pygame.display.update()
            time.sleep(1.0/self.fps)


if __name__ == "__main__":
    pygame.init()
    Game(80, 45).play()
