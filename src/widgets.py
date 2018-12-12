BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
WHITE = (240, 240, 240)
RED = (240, 10, 10)
GREEN = (10, 240, 100)


class Timer:
    def __init__(self, period, callback):
        self.period = period
        self.callback = callback
        self.active = True

    def tick(self):
        self.period -= 1
        if self.period == 0:
            self.callback()
            self.active = False
    
    def is_active(self):
        return self.active


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


class Window(Widget):
    pass

class Scene(Widget):
    pass

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


# TODO Window
# TODO Scene
# TODO Сheckbox
# TODO LineEdit
# TODO TextList
