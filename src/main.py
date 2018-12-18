import pygame
import sys
import time
import yaml
from widgets import Widget, Window, Scene, Menu, Label, Signal, Color, ColorRole
from gui import GUI
from game import Game


KEYS = {pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)}


class MainWindow(Window):
    def __init__(self, gui):
        super().__init__(gui.rect, gui.draw_menu)
        self.gui = gui
        path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
        with open(path, 'r') as file:
            self.config = yaml.load(file)
        file.close()
        self.form = Menu(self.rect, gui.draw_menu, self.config["MainMenu"])
        self.fps = 20
        self.last_game = None
        self.highscore = 0

    def update(self, signal):
        self.fps = 20
        if signal == Signal.PauseGame:
            self.last_game = self.form
            self.form = Menu(self.rect, gui.draw_menu, self.config["PauseMenu"])
        elif signal == Signal.ContinueGame:
            self.form = self.last_game
            self.form.redraw(self.form)
            self.fps = 8
        elif signal == Signal.OpenMainMenu:
            self.form = Menu(self.rect, gui.draw_menu, self.config["MainMenu"])
        elif signal == Signal.OpenEvolutionMenu:
            self.form = Menu(self.rect, gui.draw_menu, self.config["EvolutionMenu"])
        elif signal == Signal.StartNewGame:
            self.form = GameForm(self.rect, gui.draw_game, gui.cell_size)
            self.fps = 8


class GameForm(Scene):
    def __init__(self, rect, redraw, cell_size):
        super().__init__(rect, redraw)
        self.cell_size = cell_size
        x, y, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score = Label((w*0.4, 0, h*0.2, h*0.2), '0')
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY
        self.redraw(self)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Signal.PauseGame
                if event.key in KEYS:
                    self.game.snake_mind.desire(KEYS[event.key])
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            return Signal.OpenMainMenu
        self.redraw(self)


if __name__ == "__main__":
    gui = GUI(80, 40, 10)
    main_window = MainWindow(gui)
    # events = list()
    playing = True
    while playing:
        events = gui.check_events()
        for event in events:
            if event.type == pygame.QUIT:
                playing = False
        signal = main_window.form.update(events)
        if signal is not None:
            main_window.update(signal)

        # events += gui.check_events()
        # events = main_window.update(events)

        pygame.display.update()
        time.sleep(1.0/main_window.fps)
