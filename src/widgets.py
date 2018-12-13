import yaml
from enum import Enum


class Widget:
    class Color(Enum):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        RED = (250, 10, 10)

    class ColorRole(Enum):
        Background = 0
        Foreground = 1
        Text = 2

    class State(Enum):
        Active = 0
        Inactive = 1
        Highlighted = 2
        Pressed = 3

    class Signal(Enum):
        Pressed = 0
        Input_finished = 1
        Exit = 2

    class Event(Enum):
        pass

    @staticmethod
    def load(path: str):
        pass

    @staticmethod
    def default_colors():
        State, Role, Color = Widget.State, Widget.ColorRole, Widget.Color
        return {
            State.Active: {
                Role.Background: Color.BLACK,
                Role.Foreground: Color.GRAY,
                Role.Text: Color.WHITE
            },
            State.Inactive: {
                Role.Background: Color.BLACK,
                Role.Foreground: Color.DARK_GRAY,
                Role.Text: Color.BLACK
            },
            State.Highlighted: {
                Role.Background: Color.BLACK,
                Role.Foreground: Color.WHITE,
                Role.Text: Color.GRAY
            },
            State.Pressed: {
                Role.Background: Color.BLACK,
                Role.Foreground: Color.RED,
                Role.Text: Color.BLACK
            }
        }

    def __init__(self, rect: (float, float, float, float)):
        self.rect = rect
        self.__focusable = False
        self.children = list()
        self.__active = True
        self.__painter = None
        self.__callbacks = dict()
        self.__colors = Widget.default_colors()

    def set_color(self, state: Widget.State, role: Widget.ColorRole, color: Widget.Color):
        if not isinstance(color, Widget.Color):
            raise "Unknown color"
        if state not in self.__colors:
            raise "No such state"
        if role not in self.__colors[state]:
            raise "No such role"
        self.__colors[state][role] = color

    def get_color(self, state: Widget.State, role: Widget.ColorRole,):
        return self.__colors[state][role]

    def set_painter(self, painter: object):
        self.__painter = painter

    def draw(self):
        if self.__painter is None:
            raise "No painter specified"
        self.__painter.draw(self)
        for child in self.children:
            child.draw()

    def set_callback(self, signal: Widget.Signal, callback: callable):
        if not isinstance(signal, Widget.Signal):
            raise "Unknown signal"
        self.__callbacks[signal] = callback

    def add_child(self, child: Widget):
        x, y, w, h = child.rect
        if not self.inside(x, y) or not self.inside(x + w, y + h):
            raise "Child is outside of parent"
        self.children.append(child)

    def get_children(self):
        return self.children

    def inside(self, cx: float, cy: float):
        x, y, w, h = self.rect
        return x < cx < x + w and y < cy < y + h

    def is_focusable(self):
        return self.__focusable and self.__active

    def set_active(self, val: bool):
        self.__active = val

    def is_active(self):
        return self.__active

    def get_state(self):
        return Widget.State.Active if self.__active else Widget.State.Inactive

class Button(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text
        self.__focusable = True
        self.__pressed = False
        self.__highlighted = False

    def press(self):
        if not self.__active:
            return
        self.__pressed = True

    def release(self):
        self.__pressed = False

    def check_state(self, mouse_pressed, mouse_released, mouse_on_button):
        if not self.__active:
            return
        ret = False
        if mouse_on_button and mouse_pressed:
            self.press()
        if self.__pressed and mouse_released:
            self.release()
            if mouse_on_button:
                ret = True
        if ret and Widget.Signal.Pressed in self.__callbacks:
            self.__callbacks[Widget.Signal.Pressed]()
        return ret

    def highlight(self):
        if not self.__highlighted and self.__active:
            self.__highlighted = True

    def diminish(self):
        if self.__highlighted and self.__active:
            self.__highlighted = False

    def is_highlighted(self):
        return self.__highlighted

    def get_state(self):
        if self.__pressed:
            ret = Widget.State.Pressed
        elif not self.__active:
            ret = Widget.State.Inactive
        else:
            if self.__highlighted:
                ret = Widget.State.Highlighted
            else:
                ret = Widget.State.Active
        return ret

class Label(Widget):
    pass

class Window(Widget):
    pass