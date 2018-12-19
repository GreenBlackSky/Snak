import pygame
from widgets import Window, Button, Menu, Label
from colors import Color, ColorRole
from events import Event

class GUI:
    def __init__(self, width, height, cell_size=10):
        pygame.init()
        width, height = width*cell_size, height*cell_size
        self.cell_size = cell_size
        self.mouse_pressed = False
        self.screen = pygame.display.set_mode((width, height))
        self.rect = (0, 0, width, height)

    def draw_button(self, button):
        fore_color = button.palette[button.state][ColorRole.Foreground].value
        text_color = button.palette[button.state][ColorRole.Text].value
        pygame.draw.rect(self.screen, fore_color, button.rect, 0)
        x, y, w, h = button.rect
        font = pygame.font.SysFont("monospace", int(h/3))
        label = font.render(button.text, 1, text_color)
        tx, ty, tw, th = label.get_rect()
        label_pos = (x + max((w - tw)/2, 0), \
                    y + max((h - th)/2, 0))
        self.screen.blit(label, label_pos)

    def draw_label(self, label):
        fore_color = label.palette[label.state][ColorRole.Foreground].value
        text_color = label.palette[label.state][ColorRole.Text].value
        pygame.draw.rect(self.screen, fore_color, label.rect, 0)
        x, y, w, h = label.rect
        font = pygame.font.SysFont("monospace", int(h))
        surface = font.render(label.text, 1, text_color)
        tx, ty, tw, th = surface.get_rect()
        label_pos = (x + max((w - tw)/2, 0), \
                    y + max((h - th)/2, 0))
        self.screen.blit(surface, label_pos)

    def draw_menu(self, menu):
        self.screen.fill(Color.BLACK.value)
        for widget in menu.widgets:
            if type(widget) == Button:
                self.draw_button(widget)
            elif type(widget) == Label:
                self.draw_label(widget)

    def draw_game(self, game):
        self.screen.fill(Color.BLACK.value)
        self.draw_label(game.score)
        self.draw_cell(game.game.food_pos, Color.RED.value)
        for cell in game.game.snake.cells:
            self.draw_cell(cell, Color.GRAY.value)
        self.draw_cell(game.game.snake.head, Color.WHITE.value)

    def draw_cell(self, pos, color):
        x, y = pos
        rect = (x*self.cell_size, \
                y*self.cell_size, \
                self.cell_size, \
                self.cell_size)
        pygame.draw.rect(self.screen, color, rect, 0)

    def update(self):
        pygame.display.update()

    def check_events(self):
        keys = {
            pygame.K_RETURN:    Event.Key.K_RETURN,
            pygame.K_ESCAPE:    Event.Key.K_ESCAPE,
            pygame.K_UP:        Event.Key.K_UP,
            pygame.K_DOWN:      Event.Key.K_DOWN,
            pygame.K_RIGHT:     Event.Key.K_RIGHT,
            pygame.K_LEFT:      Event.Key.K_LEFT,
        }
        ret = list()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in keys:
                ret.append(Event(Event.Type.KeyPressed, keys[event.key]))
            elif event.type == pygame.KEYUP and event.key in keys:
                ret.append(Event(Event.Type.KeyReleased, keys[event.key]))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pressed = True
                x, y = pygame.mouse.get_pos()
                ret.append(Event(Event.Type.MousePressed, (x, y)))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_pressed = False
                x, y = pygame.mouse.get_pos()
                ret.append(Event(Event.Type.MouseReleased, (x, y, self.mouse_pressed)))
            elif event.type == pygame.QUIT:
                ret.append(Event(Event.Type.Quit))
        x, y = pygame.mouse.get_pos()
        ret.append(Event(Event.Type.MouseState, (x, y, self.mouse_pressed)))
        return ret

# TODO draw_scene instead of game