import pygame
from widgets import *


class GUI:
    def __init__(self, width, height):
        pygame.init()
        self.cell_size = 10
        self.screen = pygame.display.set_mode((width*self.cell_size, height*self.cell_size))

    def draw_button(self, button: Button):
        foreground = button.get_color(button.get_state(), Widget.ColorRole.Foreground)
        text_color = button.get_color(button.get_state(), Widget.ColorRole.Text)

        pygame.draw.rect(self.screen, foreground, button.rect, 0)
        x, y, w, h = button.rect
        font = pygame.font.SysFont("monospace", int(h/3))
        label = font.render(button.text, 1, text_color)
        tx, ty, tw, th = label.get_rect()
        label_pos = (x + max((w - tw)/2, 0), y + max((h - th)/2, 0))
        self.screen.blit(label, label_pos)

    def draw_label(self, label: Label):
        pass

    def draw_window(self, window: Window):
        pass

    def draw(self, widget: Widget):
        pass

    def get_events(self):
        pass

    def update(self):
        pygame.display.update()