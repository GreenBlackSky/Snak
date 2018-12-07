
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (240, 240, 240)
RED = (240, 10, 10)

class Widget:
    def __init__(self, rect):
        self.rect = rect
        self.highlighted = False
        self.first_color = GRAY
        self.second_color = WHITE

    def highlight(self):
        if not self.highlighted:
            self.highlighted = True
            self.first_color = WHITE
            self.second_color = GRAY

    def diminish(self):
        if self.highlighted:
            self.highlighted = False
            self.first_color = GRAY
            self.second_color = WHITE

    def inside(self, cx, cy):
        x, y, w, h = self.rect
        return x < cx < x + w and y < cy < y + h


class Button(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text
        self.pressed = False

    def press(self):
        self.first_color = RED
        self.second_color = BLACK
        self.pressed = True

    def release(self):
        self.first_color = GRAY
        self.second_color = WHITE
        self.pressed = False

    def check_state(self, mouse_pressed, mouse_released, mouse_on_button):
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

# TODO inactive widgets
# TODO checkbox
# TODO text field
# TODO list
# TODO move colors to separate file
# TODO make widget colors editable
