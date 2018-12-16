import sys
import pygame
import time
from widgets import *


class GUI:
    KEYS = {pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)}

    def draw_button(self, button):
        pygame.draw.rect(self.screen, button.first_color, button.rect, 0)
        x, y, w, h = button.rect
        font = pygame.font.SysFont("monospace", int(h/3))
        label = font.render(button.text, 1, button.second_color)
        tx, ty, tw, th = label.get_rect()
        label_pos = (x + max((w - tw)/2, 0), \
                    y + max((h - th)/2, 0))
        self.screen.blit(label, label_pos)

    def draw_label(self, label):
        pygame.draw.rect(self.screen, label.first_color, label.rect, 0)
        x, y, w, h = label.rect
        font = pygame.font.SysFont("monospace", int(h/3))
        surface = font.render(label.text, 1, label.second_color)
        tx, ty, tw, th = surface.get_rect()
        label_pos = (x + max((w - tw)/2, 0), \
                    y + max((h - th)/2, 0))
        self.screen.blit(surface, label_pos)

    def draw_menu(self, menu):
        self.screen.fill(BLACK)
        for widget in menu.widgets:
            if type(widget) == Button:
                self.draw_button(widget)
            elif type(widget) == Label:
                self.draw_label(widget)

    def draw_game(self, game):
        self.screen.fill(BLACK)
        self.draw_score(game.score)
        self.draw_cell(game.food_pos, RED)
        for cell in game.snake.cells:
            self.draw_cell(cell, GRAY)
        self.draw_cell(game.snake.head, WHITE)

    def draw_cell(self, pos, color):
        x, y = pos
        rect = (x*self.cell_size, \
                y*self.cell_size, \
                self.cell_size, \
                self.cell_size)
        pygame.draw.rect(self.screen, color, rect, 0)

    def draw_score(self, score):
        x, y, w, h = self.screen.get_rect()
        font = pygame.font.SysFont("monospace", int(h/2))
        label = font.render(str(score), 1, DARK_GRAY, BLACK)
        tx, ty, tw, th = label.get_rect()
        label_pos = (max((w - tw)/2, 0), 0)
        self.screen.blit(label, label_pos)

    def __init__(self, width, height, cell_size=10):
        pygame.init()
        self.width, self.height, self.cell_size = width*cell_size, height*cell_size, cell_size
        self.screen = pygame.display.set_mode((width*self.cell_size, height*self.cell_size))
        self.path = sys.argv[1] if len(sys.argv) > 1 else None
        self.form = Menu(self.width, self.height, self.draw_menu, "MainMenu", self.path)
        self.fps = 20
        self.last_game = None
        self.highscore = 0

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
        if signal == Signal.PauseGame:
            self.last_game = self.form
            self.form = Menu(self.width, self.height, self.draw_menu, "PauseMenu", self.path)
        elif signal == Signal.ContinueGame:
            self.form = self.last_game
            self.form.redraw(self.form.game)
            self.fps = 8
        elif signal == Signal.OpenMainMenu:
            self.form = Menu(self.width, self.height, self.draw_menu, "MainMenu", self.path)
        elif signal == Signal.OpenEvolutionMenu:
            self.form = Menu(self.width, self.height, self.draw_menu, "EvolutionMenu", self.path)
        elif signal == Signal.StartNewGame:
            self.form = GameForm(self.width, self.height, self.draw_game, self.cell_size)
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

# TODO add highscore
# TODO add you-loose-menu
# TODO add new-highscore-menu
# TODO add scale choise
# TODO add speed choise
# TODO open file safely
