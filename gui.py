import sys, pygame, time


class GUI:
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)
    WHITE = (240, 240, 240)
    RED = (240, 10, 10)

    KEYS = {pygame.K_UP: (0, -1), \
            pygame.K_DOWN: (0, 1), \
            pygame.K_LEFT: (-1, 0), \
            pygame.K_RIGHT: (1, 0)}


    class Widget:
        def __init__(self, rect):
            self.rect = rect
            self.highlighted = False
            self.first_color = GUI.GRAY
            self.second_color = GUI.WHITE

        def highlight(self):
            if not self.highlighted:
                self.highlighted = True
                self.first_color = GUI.WHITE
                self.second_color = GUI.GRAY
        
        def diminish(self):
            if self.highlighted:
                self.highlighted = False
                self.first_color = GUI.GRAY
                self.second_color = GUI.WHITE


    class Button(Widget):
        def __init__(self, rect, text):
            super().__init__(rect)
            self.text = text
            self.pressed = False

        def press(self):
            self.first_color = GUI.RED
            self.second_color = GUI.BLACK
            self.pressed = True

        def release(self):
            self.first_color = GUI.GRAY
            self.second_color = GUI.WHITE
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


    class Form:
        def __init__(self, screen, font):
            self.screen = screen
            self.screen.fill(GUI.BLACK)
            self.font = font
            self.focus = None
            x, y, self.width, self.height = self.screen.get_rect()
            self.widgets = dict()

        def draw_button(self, button):
            pygame.draw.rect(self.screen, button.first_color, button.rect, 0)
            x, y, w, h = button.rect
            label = self.font.render(button.text, 1, button.second_color)
            tx, ty, tw, th = label.get_rect()
            label_pos = (x + max((w - tw)/2, 0), \
                        y + max((h - th)/2, 0))
            self.screen.blit(label, label_pos)

        def update(self, events):
            mouse_pressed = False
            mouse_released = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_released = True

            ret = None
            mx, my = pygame.mouse.get_pos()
            fx, fy, fw, fh = self.focus.rect
            mouse_on_focus = (fx < mx < fx + fw and fy < my < fy + fh)
            if self.focus.check_state(mouse_pressed, mouse_released, mouse_on_focus):
                ret = self.widgets[self.focus]

            if not self.focus.pressed:
                for widget in self.widgets:
                    widget.diminish()
                    x, y, w, h = widget.rect
                    mouse_on_widget = (x < mx < x + w and y < my < y + h)
                    if mouse_on_widget:
                        self.focus = widget

            self.focus.highlight()
            self.redraw()
            return ret
        
        def redraw(self):
            for widget in self.widgets:
                if type(widget) == GUI.Button:
                    self.draw_button(widget)


    class MainMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.focus = GUI.Button((self.width*(2.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "START")
            self.widgets[self.focus] = GUI.PauseMenu
            self.widgets[GUI.Button((self.width*(2.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "EVOLVE")] = GUI.EvolutionMenu
            self.focus.highlight()
            self.redraw()


    class PauseMenu(Form):
        def __init__(self, screen, font, callback):
            super().__init__(screen, font)
            self.focus = GUI.Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Continue")
            self.widgets[self.focus] = None
            self.widgets[GUI.Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Restart")] = None
            self.widgets[GUI.Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Back")] = callback
            self.focus.highlight()
            self.redraw()


    class EvolutionMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.focus = GUI.Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Start")
            self.widgets[self.focus] = GUI.PauseMenu
            self.widgets[GUI.Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Pause")] = None
            self.widgets[GUI.Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Watch")] = None
            self.widgets[GUI.Button((self.width*(1.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "Back")] = GUI.MainMenu
            self.focus.highlight()
            self.redraw()


    class Game(Form):
        def __init__(self, screen, font, cell_size):
            super().__init__(screen, font)
            self.cell_size = cell_size

        def draw_cell(self, pos, color):
            x, y = pos
            rect = (x*self.cell_size, \
                    y*self.cell_size, \
                    self.cell_size, \
                    self.cell_size)
            pygame.draw.rect(self.screen, color, rect, 0)

        def update(self):
            pass


    def __init__(self, width, height, cell_size=10):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", width//4)
        self.cell_size = cell_size
        self.field_width, self.field_height = width, height
        self.screen_width, self.screen_height = self.field_width*self.cell_size, self.field_height*self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.form = GUI.MainMenu(self.screen, self.font)

    def exec(self):
        events = list()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    events.append(event)
            next_form = self.form.update(events)
            events.clear()

            if next_form is not None:
                if next_form == GUI.PauseMenu:
                    self.form = GUI.PauseMenu(self.screen, self.font, type(self.form))
                elif next_form == GUI.MainMenu:
                    self.form = GUI.MainMenu(self.screen, self.font)
                elif next_form == GUI.EvolutionMenu:
                    self.form = GUI.EvolutionMenu(self.screen, self.font)

            time.sleep(0.05)
            pygame.display.update()


if __name__ == "__main__":
    GUI(80, 45).exec()