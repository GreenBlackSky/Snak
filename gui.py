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


    class Button(Widget):
        def __init__(self, rect, text):
            super().__init__(rect)
            self.text = text
            self.highlighted = False
            self.pressed = False
            self.color, self.text_color =  GUI.GRAY, GUI.WHITE

        def invert(self):
            self.highlighted = not self.highlighted
            self.color, self.text_color = self.text_color, self.color

        def press(self):
            self.color = GUI.RED
            self.pressed = True

        def release(self):
            self.color = GUI.WHITE
            self.text_color = GUI.GRAY
            self.pressed = False

        def check_state(self, mouse_pressed, mouse_released):
            ret = False
            x, y, w, h = self.rect
            mx, my = pygame.mouse.get_pos()
            mouse_on_button = (x < mx < x + w and y < my < y + h)
            if not self.pressed and ((mouse_on_button and not self.highlighted) or (self.highlighted and not mouse_on_button)):
                self.invert()
            if mouse_on_button and mouse_pressed:
                self.press()
            if self.pressed and mouse_released:
                self.release()
                if mouse_on_button:
                    ret = True
            return ret


    class TextList(Widget):
        pass


    class TextInput(Widget):
        pass


    class Form:
        def __init__(self, screen, font):
            self.screen = screen
            self.screen.fill(GUI.BLACK)
            self.font = font
            x, y, self.width, self.height = self.screen.get_rect()

        def draw_button(self, button):
            pygame.draw.rect(self.screen, button.color, button.rect, 0)
            x, y, w, h = button.rect
            label = self.font.render(button.text, 1, button.text_color)
            tx, ty, tw, th = label.get_rect()
            label_pos = (x + max((w - tw)/2, 0), \
                        y + max((h - th)/2, 0))
            self.screen.blit(label, label_pos)


    class MainMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.start_button = GUI.Button((self.width*(2.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "START")
            self.evolve_button = GUI.Button((self.width*(2.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "EVOLVE")
            self.redraw()

        def update(self, mouse_pressed, mouse_released):
            ret = None
            if self.start_button.check_state(mouse_pressed, mouse_released):
                ret = GUI.PauseMenu
            if self.evolve_button.check_state(mouse_pressed, mouse_released):
                ret = GUI.EvolutionMenu
            self.redraw()
            return ret

        def redraw(self):
            self.draw_button(self.start_button)
            self.draw_button(self.evolve_button)

    class PauseMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.continue_button = GUI.Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Continue")
            self.restart_button = GUI.Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Restart")
            self.main_menu_button = GUI.Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Back")
            self.redraw()

        def update(self, mouse_pressed, mouse_released):
            ret = None
            self.continue_button.check_state(mouse_pressed, mouse_released)
            self.restart_button.check_state(mouse_pressed, mouse_released)
            if self.main_menu_button.check_state(mouse_pressed, mouse_released):
                ret = GUI.MainMenu
            self.redraw()
            return ret

        def redraw(self):
            self.draw_button(self.continue_button)
            self.draw_button(self.restart_button)
            self.draw_button(self.main_menu_button)

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

    class EvolutionMenu(Form):
        def __init__(self, screen, font):
            super().__init__(screen, font)
            self.start_button = GUI.Button((self.width*(1.0/5), 0, self.width/5.0, self.height/5.0), "Start")
            self.pause_button = GUI.Button((self.width*(1.0/5), self.height*(1.0/5), self.width/5.0, self.height/5.0), "Pause")
            self.watch_button = GUI.Button((self.width*(1.0/5), self.height*(2.0/5), self.width/5.0, self.height/5.0), "Watch")
            self.main_menu_button = GUI.Button((self.width*(1.0/5), self.height*(3.0/5), self.width/5.0, self.height/5.0), "Back")
            self.redraw()

        def update(self, mouse_pressed, mouse_released):
            ret = None
            if self.start_button.check_state(mouse_pressed, mouse_released):
                ret = GUI.PauseMenu
            self.pause_button.check_state(mouse_pressed, mouse_released)
            self.watch_button.check_state(mouse_pressed, mouse_released)
            if self.main_menu_button.check_state(mouse_pressed, mouse_released):
                ret = GUI.MainMenu
            self.redraw()
            return ret

        def redraw(self):
            self.draw_button(self.start_button)
            self.draw_button(self.pause_button)
            self.draw_button(self.watch_button)
            self.draw_button(self.main_menu_button)

    def __init__(self, width, height, cell_size=10):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", width//4)
        self.cell_size = cell_size
        self.field_width, self.field_height = width, height
        self.screen_width, self.screen_height = self.field_width*self.cell_size, self.field_height*self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.form = GUI.MainMenu(self.screen, self.font)

    def exec(self):
        prev_form = type(self.form)
        while True:
            mouse_pressed = False
            mouse_released = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_released = True

            next_form = self.form.update(mouse_pressed, mouse_released)

            if next_form is not None:
                cur_form = type(self.form)

                if next_form == GUI.MainMenu and cur_form == GUI.PauseMenu:
                    if prev_form == GUI.MainMenu:
                        self.form = GUI.MainMenu(self.screen, self.font)
                    else:
                        self.form = GUI.EvolutionMenu(self.screen, self.font)

                elif next_form == GUI.MainMenu and cur_form == GUI.EvolutionMenu:
                    self.form = GUI.MainMenu(self.screen, self.font)

                elif next_form == GUI.PauseMenu:
                    self.form = GUI.PauseMenu(self.screen, self.font)

                elif next_form == GUI.EvolutionMenu:
                    self.form = GUI.EvolutionMenu(self.screen, self.font)
                prev_form = cur_form
            
            time.sleep(0.05)
            pygame.display.update()


if __name__ == "__main__":
    GUI(160, 90).exec()