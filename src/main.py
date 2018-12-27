import sys
import time
import yaml
from widgets import Widget, Scene, Layout, Label, Signal
from events import Event
from colors import Color, ColorRole
from gui import GUI
from game import Game


KEYS = {Event.Key.K_UP: (0, -1),
        Event.Key.K_DOWN: (0, 1),
        Event.Key.K_LEFT: (-1, 0),
        Event.Key.K_RIGHT: (1, 0)}


class MainWindow(Layout):
    def __init__(self, gui, config):
        super().__init__(gui.rect, gui.draw_menu)
        self.gui = gui
        self.config = config
        self.layout = Layout(self.rect, gui.draw_menu, self.config["MainMenu"])
        self.layouts = {
            "MainMenu": Layout(self.rect, gui.draw_menu, self.config["MainMenu"]),
            "PauseMenu": Layout(self.rect, gui.draw_menu, self.config["PauseMenu"]),
            "EvolutionMenu": Layout(self.rect, gui.draw_menu, self.config["EvolutionMenu"]),
            "Game": GameForm(gui, gui.cell_size)
        }
        self.fps = 20
        self.highscore = 0

    def update(self, signal):
        self.fps = 20
        if signal == Signal.PauseGame:
            self.pause_game()
        elif signal == Signal.ContinueGame:
            self.continue_game()
        elif signal == Signal.OpenMainMenu:
            self.open_main_menu()
        elif signal == Signal.OpenEvolutionMenu:
            self.open_evolution_menu()
        elif signal == Signal.StartNewGame:
            self.start_new_game()

    def pause_game(self):
        self.fps = 20
        self.layout = self.layouts["PauseMenu"]

    def continue_game(self):
        self.layout = self.layouts["Game"]
        self.fps = 8

    def open_main_menu(self):
        self.fps = 20
        self.layout = self.layouts["MainMenu"]

    def open_evolution_menu(self):
        self.fps = 20
        self.layout = self.layouts["EvolutionMenu"]

    def start_new_game(self):
        self.layout = self.layouts["Game"]
        self.layout.reset()
        self.fps = 8


class GameForm(Scene):
    def __init__(self, gui, cell_size):
        super().__init__(gui.rect, gui.draw_game)
        self.cell_size = cell_size
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score = Label((w*0.4, 0, h*0.2, h*0.2), '0')
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY
        self.redraw(self)

    def update(self, events):
        for event in events:
            if event.type == Event.Type.KeyPressed:
                if event.data == Event.Key.K_ESCAPE:
                    return Signal.PauseGame
                if event.data in KEYS:
                    self.game.snake_mind.desire(KEYS[event.data])
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            return Signal.OpenMainMenu
        self.redraw(self)

    def reset(self):
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score.text = "0"
        self.game.score = 0


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    file = open(path, 'r')
    config = yaml.load(file)
    file.close()
    gui = GUI(80, 40, 10)
    main_window = MainWindow(gui, config)
    # events = list()
    playing = True
    while playing:
        events = gui.check_events()
        for event in events:
            if event.type == Event.Type.Quit:
                playing = False
        signal = main_window.layout.update(events)
        if signal is not None:
            main_window.update(signal)

        # events += gui.check_events()
        # events = main_window.update(events)

        gui.update()
        time.sleep(1.0/main_window.fps)
