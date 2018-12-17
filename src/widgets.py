import pygame
from enum import Enum

class Colors(Enum):
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)
    WHITE = (240, 240, 240)
    RED = (240, 10, 10)
    GREEN = (10, 240, 100)


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
        self.first_color = Colors.GRAY
        self.second_color = Colors.WHITE
        self.active = True

    def inside(self, cx, cy):
        x, y, w, h = self.rect
        return x < cx < x + w and y < cy < y + h

    def is_focusable(self):
        return self.focusable and self.active

    def set_active(self, val):
        self.active = val
        if not self.active:
            self.first_color = Colors.DARK_GRAY
            self.second_color = Colors.BLACK
        else:
            self.first_color = Colors.GRAY
            self.second_color = Colors.WHITE

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
        self.first_color = Colors.RED
        self.second_color = Colors.BLACK
        self.pressed = True

    def release(self):
        if not self.active:
            return
        self.first_color = Colors.GRAY
        self.second_color = Colors.WHITE
        self.pressed = False

    def highlight(self):
        if not self.highlighted and self.active:
            self.highlighted = True
            self.first_color = Colors.WHITE
            self.second_color = Colors.GRAY

    def diminish(self):
        if self.highlighted and self.active:
            self.highlighted = False
            self.first_color = Colors.GRAY
            self.second_color = Colors.WHITE

    def update(self, mouse_pressed, mouse_released, mouse_on_button):
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
        self.first_color = Colors.BLACK


class CheckBox(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class Window(Widget):
    def __init__(self, rect, redraw):
        super().__init__(rect)
        self.redraw = redraw
        self.focus = None
        self.widgets = []
        self.focus_order = []
        self.callbacks = {}


class Menu(Window):
    def __init__(self, rect, redraw, config):
        super().__init__(rect, redraw)
        x, y, w, h = self.rect
        for widget_cfg in config:
            # Create widget
            xm, ym, wm, hm = widget_cfg["rect"]
            rect = (x + w*xm, y + h*ym, w*wm, h*hm)
            widget = eval(widget_cfg["type"])(rect, widget_cfg["capture"])
            # Activate widget
            if not widget_cfg.get("active", True):
                widget.set_active(False)
            # Add widget to focus_order and widgets
            self.widgets.append(widget)
            if widget.is_focusable():
                self.focus_order.append(widget)
            # set callback
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
            ret = self.callbacks[self.focus]
        mx, my = pygame.mouse.get_pos()
        if self.focus.update(mouse_pressed, mouse_released, self.focus.inside(mx, my)):
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


class Scene(Window):
    def __init__(self, rect, redraw):
        super().__init__(rect, redraw)

# TODO Colors
# TODO events
# TODO load
# TODO redraw