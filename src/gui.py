import sys
import pygame
import time
import yaml
from game import Game
from widgets import *
from enum import Enum


class GUI:
    KEYS = {pygame.K_UP: (0, -1), \
            pygame.K_DOWN: (0, 1), \
            pygame.K_LEFT: (-1, 0), \
            pygame.K_RIGHT: (1, 0)}

    WIDGET_TYPES = {"Button": Button}

    class Signal(Enum):
        StartNewGame = 0,
        PauseGame = 1,
        OpenEvolutionMenu = 2,
        ContinueGame = 3,
        OpenMainMenu = 4,
        YouLoose = 5,
        NewHighScore = 6

    class Form:
        def __init__(self, screen):
            self.screen = screen
            self.screen.fill(BLACK)
            self.focus = None
            x, y, self.width, self.height = self.screen.get_rect()
            self.widgets = []
            self.callbacks = {}

        def initialize(self, widget):
            self.focus = widget
            widget.highlight()
            self.redraw()

        def draw_button(self, button):
            pygame.draw.rect(self.screen, button.first_color, button.rect, 0)
            x, y, w, h = button.rect
            font = pygame.font.SysFont("monospace", int(h/3))
            label = font.render(button.text, 1, button.second_color)
            tx, ty, tw, th = label.get_rect()
            label_pos = (x + max((w - tw)/2, 0), \
                        y + max((h - th)/2, 0))
            self.screen.blit(label, label_pos)

        def map_events(self, events):
            mouse_pressed = False
            mouse_released = False
            focus_n = self.widgets.index(self.focus)
            return_pressed = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_released = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        focus_n -= 1
                    if event.key == pygame.K_DOWN:
                        focus_n += 1
                    if event.key == pygame.K_RETURN:
                        return_pressed = True
            focus_n = max(focus_n, 0)
            focus_n = min(focus_n, len(self.widgets) - 1)
            return mouse_pressed, mouse_released, focus_n, return_pressed

        def update(self, events):
            mouse_pressed, mouse_released, focus_n, return_pressed = self.map_events(events)
            # Check focus
            ret = None
            if return_pressed:
                ret = self.callbacks[self.focus]
            mx, my = pygame.mouse.get_pos()
            if self.focus.check_state(mouse_pressed, mouse_released, self.focus.inside(mx, my)):
                ret = self.callbacks[self.focus]
            # Move focus
            if not self.focus.pressed:
                old_focus = self.focus
                for widget in self.widgets:
                    widget.diminish()
                    if widget.inside(mx, my):
                        self.focus = widget
                if old_focus == self.focus:
                    self.focus = self.widgets[focus_n]
            # Redraw
            self.focus.highlight()
            self.redraw()
            return ret

        def redraw(self):
            for widget in self.widgets:
                if type(widget) == Button:
                    self.draw_button(widget)

    class Menu(Form):
        def __init__(self, screen, menu_type):
            super().__init__(screen)
            config = yaml.load(open("cfg/menu.yaml", 'r'))
            for widget_cfg in config[menu_type]:
                widget_type = GUI.WIDGET_TYPES[widget_cfg["type"]]
                rect = (self.width*widget_cfg['x'],
                        self.height*widget_cfg['y'],
                        self.width*widget_cfg['w'],
                        self.height*widget_cfg['h'])
                widget = widget_type(rect, widget_cfg["capture"])
                self.widgets.append(widget)
                if widget_cfg["callback"] == "None":
                    self.callbacks[widget] = None
                else:
                    self.callbacks[widget] = GUI.Signal[widget_cfg["callback"]]
            self.focus = self.widgets[0]
            self.focus.highlight()
            self.redraw()

    class GameForm(Form):
        def __init__(self, screen, cell_size):
            super().__init__(screen)
            self.cell_size = cell_size
            self.game = Game(self.width//self.cell_size, self.height//self.cell_size)
            self.redraw()

        def draw_cell(self, pos, color):
            x, y = pos
            rect = (x*self.cell_size, \
                    y*self.cell_size, \
                    self.cell_size, \
                    self.cell_size)
            pygame.draw.rect(self.screen, color, rect, 0)

        def draw_score(self):
            font = pygame.font.SysFont("monospace", int(self.height/2))
            label = font.render(str(self.game.score), 1, GRAY, BLACK)
            tx, ty, tw, th = label.get_rect()
            label_pos = (max((self.width - tw)/2, 0), 0)
            self.screen.blit(label, label_pos)
        
        def update(self, events):
            # Check events
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return GUI.Signal.PauseGame
                    if event.key in GUI.KEYS:
                        self.game.snake_mind.desire(GUI.KEYS[event.key])
            self.draw_cell(self.game.snake.head, GRAY)
            # Move snake
            food_pos = self.game.food_pos
            self.game.make_move(self.game.get_next_move())
            if self.game.food_pos != food_pos:
                self.draw_cell(self.game.food_pos, RED)
                self.draw_score()
            # Check for Gameover
            if self.game.snake.is_selfcrossed():
                return GUI.Signal.OpenMainMenu
            # Redraw screen
            self.draw_cell(self.game.snake.tail, BLACK)
            self.draw_cell(self.game.snake.head, WHITE)

        def redraw(self):
            self.screen.fill(BLACK)
            self.draw_score()
            self.draw_cell(self.game.food_pos, RED)
            for cell in self.game.snake.cells:
                self.draw_cell(cell, WHITE)

    def __init__(self, width, height, cell_size=10):
        pygame.init()
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((width*self.cell_size, height*self.cell_size))
        self.form = GUI.Menu(self.screen, "MainMenu")
        self.fps = 20
        self.last_game = None

    def check_events(self):
        ret = list()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                ret.append(event)
        return ret

    def update(self, signal):
        self.fps = 20
        if signal == GUI.Signal.PauseGame:
            self.last_game = self.form
            self.form = GUI.Menu(self.screen, "PauseMenu")
        elif signal == GUI.Signal.ContinueGame:
            self.form = self.last_game
            self.form.redraw()
            self.fps = 8
        elif signal == GUI.Signal.OpenMainMenu:
            self.form = GUI.Menu(self.screen, "MainMenu")
        elif signal == GUI.Signal.OpenEvolutionMenu:
            self.form = GUI.Menu(self.screen, "EvolutionMenu")
        elif signal == GUI.Signal.StartNewGame:
            self.form = GUI.GameForm(self.screen, self.cell_size)
            self.fps = 8

    def exec(self):
        while True:
            events = self.check_events()
            signal = self.form.update(events)
            if signal is not None:
                self.update(signal)
            time.sleep(1.0/self.fps)
            pygame.display.update()


if __name__ == "__main__":
    GUI(80, 40, 10).exec()

# TODO make head different color
# TODO add highscore
# TODO add you-loose-menu
# TODO add new-highscore-menu
# TODO implement score as label-widget
# TODO make score untochable
# TODO add scale choise
# TODO add speed choise
# TODO open file safely
# TODO make form widget (??)
