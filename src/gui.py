import pygame
from mwidgets import Event, Color, ColorRole


class GUI:
    def __init__(self, width, height):
        pygame.init()
        self.mouse_pressed = False
        self.screen = pygame.display.set_mode((width, height))

    def draw_rect_with_text(self, widget):
        fore_color = widget.palette[widget.state][ColorRole.Foreground].value
        text_color = widget.palette[widget.state][ColorRole.Text].value
        pygame.draw.rect(self.screen, fore_color, widget.rect, 0)
        x, y, w, h = widget.rect
        font = pygame.font.SysFont("monospace", int(h/3))
        surface = font.render(widget.text, 1, text_color)
        *_, tw, th = surface.get_rect()
        widget_pos = (x + max((w - tw)/2, 0), \
                    y + max((h - th)/2, 0))
        self.screen.blit(surface, widget_pos)

    def draw_button(self, button):
        self.draw_rect_with_text(button)

    def draw_label(self, label):
        self.draw_rect_with_text(label)

    def fill(self, color):
        self.screen.fill(color.value)

    def draw_square(self, pos, size, color):
        x, y = pos
        rect = (x*size, y*size, size, size)
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
                ret.append(Event(Event.Type.KeyPressed, data=keys[event.key]))
            elif event.type == pygame.KEYUP and event.key in keys:
                ret.append(Event(Event.Type.KeyReleased, data=keys[event.key]))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pressed = True
                x, y = pygame.mouse.get_pos()
                ret.append(Event(Event.Type.MousePressed, data=(x, y)))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_pressed = False
                x, y = pygame.mouse.get_pos()
                ret.append(Event(Event.Type.MouseReleased, data=(x, y, self.mouse_pressed)))
            elif event.type == pygame.QUIT:
                ret.append(Event(Event.Type.Quit))
        x, y = pygame.mouse.get_pos()
        ret.append(Event(Event.Type.MouseState, data=(x, y, self.mouse_pressed)))
        return ret

# TODO draw_scene instead of game
