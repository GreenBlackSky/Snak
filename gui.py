import sys, pygame, time
from game import Game
from widgets import *

class GUI:
    KEYS = {pygame.K_UP: (0, -1), \
            pygame.K_DOWN: (0, 1), \
            pygame.K_LEFT: (-1, 0), \
            pygame.K_RIGHT: (1, 0)}


    class Form:
        def __init__(self, screen, font):
            self.screen = screen
            self.screen.fill(BLACK)
            self.font = font
            self.focus = None
            x, y, self.width, self.height = self.screen.get_rect()
            self.widgets = dict()

        def draw_button(self, button):
            pygame.draw.rect(self.screen, button.first_color, button.rect, 0)
            x, y, w, h = button.rect
            label = self.font.render(button.text, 1, button.second_color)
            tx, ty, tw, th = label.get_rect()
            label_pos = (x + max((w - tw)/2, 0), \
                        y + max((h - th)/2, 0))
            self.screen.blit(label, label_pos)

        def update(self, events):
            # Check events
            mouse_pressed = False
            mouse_released = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_released = True
            # Check focus
            ret = None
            mx, my = pygame.mouse.get_pos()
            if self.focus.check_state(mouse_pressed, mouse_released, self.focus.inside(mx, my)):
                ret = self.widgets[self.focus]
            # Move focus
            if not self.focus.pressed:
                for widget in self.widgets:
                    widget.diminish()
                    if widget.inside(mx, my):
                        self.focus = widget
            # Redraw
            self.focus.highlight()
            self.redraw()
            return ret

        def redraw(self):
            for widget in self.widgets:
                if type(widget) == Button:
                    self.draw_button(widget)

    class MainMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.focus = Button((self.width*(2.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "START")
            self.widgets[self.focus] = GUI.GameForm
            self.widgets[Button((self.width*(2.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "EVOLVE")] = GUI.EvolutionMenu
            self.focus.highlight()
            self.redraw()


    class PauseMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.focus = Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Continue")
            self.widgets[self.focus] = GUI.GameForm
            self.widgets[Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Restart")] = GUI.GameForm
            self.widgets[Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Back")] = GUI.MainMenu
            self.focus.highlight()
            self.redraw()


    class EvolutionMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.focus = Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Start")
            self.widgets[self.focus] = None
            self.widgets[Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Pause")] = None
            self.widgets[Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Watch")] = GUI.GameForm
            self.widgets[Button((self.width*(1.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "Back")] = GUI.MainMenu
            self.focus.highlight()
            self.redraw()


    class GameForm(Form):
        def __init__(self, screen, font, cell_size):
            super().__init__(screen, font)
            self.cell_size = cell_size
            self.game = Game(self.width//self.cell_size, self.height//self.cell_size)
            self.draw_cell((self.width/2, self.height/2), WHITE)
            self.draw_cell(self.game.food_pos, RED)

        def draw_cell(self, pos, color):
            x, y = pos
            rect = (x*self.cell_size, \
                    y*self.cell_size, \
                    self.cell_size, \
                    self.cell_size)
            pygame.draw.rect(self.screen, color, rect, 0)

        def update(self, events):
            # Check events
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return GUI.PauseMenu
                    if event.key in GUI.KEYS:
                        self.game.snake_mind.desire(GUI.KEYS[event.key])
            # Move snake
            food_pos = self.game.food_pos
            self.game.make_move(self.game.get_next_move())
            if self.game.food_pos != food_pos:
                self.draw_cell(self.game.food_pos, RED)
            # Check for Gameover
            if self.game.snake.is_selfcrossed():
                return GUI.MainMenu
            # Redraw screen
            self.draw_cell(self.game.snake.head, WHITE)
            self.draw_cell(self.game.snake.tail, BLACK)


    def __init__(self, width, height, cell_size=10):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", width//4)
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((width*self.cell_size, height*self.cell_size))
        self.form = GUI.MainMenu(self.screen, self.font)

    def exec(self):
        events = list()
        fps = 20
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    events.append(event)
            next_form = self.form.update(events)
            events.clear()

            if next_form is not None:
                fps = 20
                if next_form == GUI.PauseMenu:
                    self.form = GUI.PauseMenu(self.screen, self.font)
                elif next_form == GUI.MainMenu:
                    self.form = GUI.MainMenu(self.screen, self.font)
                elif next_form == GUI.EvolutionMenu:
                    self.form = GUI.EvolutionMenu(self.screen, self.font)
                elif next_form == GUI.GameForm:
                    self.form = GUI.GameForm(self.screen, self.font, self.cell_size)
                    fps = 8
            time.sleep(1.0/fps)
            pygame.display.update()


if __name__ == "__main__":
    GUI(80, 40, 10).exec()

# TODO implement continuing game
# TODO move focus on keydown
# TODO do smthing on Esc
# TODO add score and highscore
# TODO add you-loose-menu
# TODO add scale choise
# TODO add speed choise

# TODO odd size causes strange behavior

# TODO move controller to separate file
# TODO add NN controller and HumanController
# TODO implement evolution algorithm
