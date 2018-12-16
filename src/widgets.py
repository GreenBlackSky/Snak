from game import Game
import pygame
import yaml
import time
from enum import Enum


BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
WHITE = (240, 240, 240)
RED = (240, 10, 10)
GREEN = (10, 240, 100)

KEYS = {pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)}

class Signal(Enum):
    StartNewGame = 0,
    PauseGame = 1,
    OpenEvolutionMenu = 2,
    ContinueGame = 3,
    OpenMainMenu = 4,
    YouLoose = 5,
    NewHighScore = 6

class Widget:
    def __init__(self, rect):
        self.rect = rect
        self.highlighted = False
        self.focusable = False
        self.first_color = GRAY
        self.second_color = WHITE
        self.active = True

    def inside(self, cx, cy):
        x, y, w, h = self.rect
        return x < cx < x + w and y < cy < y + h

    def is_focusable(self):
        return self.focusable and self.active

    def set_active(self, val):
        self.active = val
        if not self.active:
            self.first_color = DARK_GRAY
            self.second_color = BLACK
        else:
            self.first_color = GRAY
            self.second_color = WHITE

    def is_active(self):
        return self.active


class Button(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text
        self.pressed = False
        self.focusable = True

    def press(self):
        if not self.active:
            return
        self.first_color = RED
        self.second_color = BLACK
        self.pressed = True

    def release(self):
        if not self.active:
            return
        self.first_color = GRAY
        self.second_color = WHITE
        self.pressed = False

    def check_state(self, mouse_pressed, mouse_released, mouse_on_button):
        if not self.active:
            return
        ret = False
        if mouse_on_button and mouse_pressed:
            self.press()
        if self.pressed and mouse_released:
            self.release()
            if mouse_on_button:
                ret = True
        return ret

    def highlight(self):
        if not self.highlighted and self.active:
            self.highlighted = True
            self.first_color = WHITE
            self.second_color = GRAY

    def diminish(self):
        if self.highlighted and self.active:
            self.highlighted = False
            self.first_color = GRAY
            self.second_color = WHITE


class TextList(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class TextInput(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class Label(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text
        self.first_color = BLACK


class Window(Widget):
    def __init__(self, rect, redraw):
        super().__init__(rect)
        self.redraw = redraw
        self.focus = None
        self.widgets = []
        self.focus_order = []
        self.callbacks = {}

class Menu(Window):
    def __init__(self, rect, redraw, menu_type, path):
        super().__init__(rect, redraw)
        if path is None:
            path = "cfg/menu.yaml"
        x, y, w, h = self.rect
        config = yaml.load(open(path, 'r'))
        for widget_cfg in config[menu_type]:
            if widget_cfg["type"] == "Button":
                widget_type = Button
            elif widget_cfg["type"] == "Label":
                widget_type = Label
            xm, ym, wm, hm = widget_cfg["rect"]
            rect = (w*xm, h*ym, w*wm, h*hm)
            widget = widget_type(rect, widget_cfg["capture"])
            if not widget_cfg.get("active", True):
                widget.set_active(False)
            self.widgets.append(widget)
            if widget.is_focusable():
                self.focus_order.append(widget)
            if "callback" not in widget_cfg:
                self.callbacks[widget] = None
            else:
                self.callbacks[widget] = Signal[widget_cfg["callback"]]
        if not self.focus_order:
            raise "No focusable on form"
        self.focus = self.focus_order[0]
        self.focus.highlight()
        self.redraw(self)

    def map_events(self, events):
        mouse_pressed = False
        mouse_released = False
        focus_n = self.focus_order.index(self.focus)
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
        focus_n = min(focus_n, len(self.focus_order) - 1)
        return mouse_pressed, mouse_released, focus_n, return_pressed

    def update(self, events):
        mouse_pressed, mouse_released, focus_n, return_pressed = self.map_events(events)
        # Check focus
        ret = None
        if return_pressed:
            self.focus.press()
            self.redraw(self)
            pygame.display.update()
            time.sleep(0.1)
            ret = self.callbacks[self.focus]
        mx, my = pygame.mouse.get_pos()
        if self.focus.check_state(mouse_pressed, mouse_released, self.focus.inside(mx, my)):
            ret = self.callbacks[self.focus]
        # Move focus
        if not self.focus.pressed:
            old_focus = self.focus
            for widget in self.focus_order:
                widget.diminish()
                if widget.inside(mx, my):
                    self.focus = widget
            if old_focus == self.focus:
                self.focus = self.focus_order[focus_n]
        # Redraw
        self.focus.highlight()
        self.redraw(self)
        return ret

class GameForm(Window):
    def __init__(self, rect, redraw, cell_size):
        super().__init__(rect, redraw)
        self.cell_size = cell_size
        x, y, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score = Label((w*0.4, 0, h*0.2, h*0.2), '0')
        self.score.second_color = DARK_GRAY
        self.redraw(self)

    def update(self, events):
        # Check events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Signal.PauseGame
                if event.key in KEYS:
                    self.game.snake_mind.desire(KEYS[event.key])
        # Move snake
        self.game.make_move(self.game.get_next_move())
        # Check score
        self.score.text = str(self.game.score)
        # Check for Gameover
        if self.game.snake.is_selfcrossed():
            return Signal.OpenMainMenu
        # Redraw screen
        self.redraw(self)           

# TODO implement events
# TODO make form widget
# TODO separate main loop from gui