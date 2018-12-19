from enum import Enum


class Event:
    class Type(Enum):
        KeyPressed = 0
        KeyReleased = 1
        MousePressed = 2
        MouseState = 3
        MouseReleased = 4
        ButtonPressed = 5
        ButtonReleased = 6
        ButtonActivated = 7
        Quit = 8
        Custom = 9

    class Key(Enum):
        K_RETURN = 0
        K_ESCAPE = 1
        K_UP = 3
        K_DOWN = 4
        K_RIGHT = 5
        K_LEFT = 6
        K_OTHER = 7

    def __init__(self, event_type, data=None):
        self.type = event_type
        self.data = data
