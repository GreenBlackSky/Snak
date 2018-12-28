import sys
import time
import yaml
from widgets import Widget, Scene, Layout, Label
from events import Event
from colors import Color, ColorRole
from gui import GUI
from game import Game


class MainWindow(Layout):
    def __init__(self, gui, config):
        super().__init__(gui.rect, gui.draw_menu)
        self.gui = gui
        self.config = config
        self.layouts = {
            "MainMenu": Layout(self.rect, gui.draw_menu, self.config["MainMenu"]),
            "PauseMenu": Layout(self.rect, gui.draw_menu, self.config["PauseMenu"]),
            "EvolutionMenu": Layout(self.rect, gui.draw_menu, self.config["EvolutionMenu"]),
            "Game": GameForm(gui, gui.cell_size, self)
        }
        self.layout = self.layouts["MainMenu"]
        self.fps = 20
        self.highscore = 0
        self.set_callbacks()

    def set_callbacks(self):
        self.layouts["MainMenu"].callbacks["new_game_button"] = self.start_new_game
        self.layouts["MainMenu"].callbacks["open_evolution_menu_button"] = self.open_evolution_menu
        self.layouts["PauseMenu"].callbacks["continue_game_button"] = self.continue_game
        self.layouts["PauseMenu"].callbacks["start_new_game_button"] = self.start_new_game
        self.layouts["PauseMenu"].callbacks["main_menu_from_pause_button"] = self.open_main_menu

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
    KEYS = {Event.Key.K_UP: (0, -1),
            Event.Key.K_DOWN: (0, 1),
            Event.Key.K_LEFT: (-1, 0),
            Event.Key.K_RIGHT: (1, 0)}

    def __init__(self, gui, cell_size, parent):
        super().__init__(gui.rect, gui.draw_game)
        self.cell_size = cell_size
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.parent = parent
        self.score = Label((w*0.4, 0, h*0.2, h*0.2), '0')
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY
        self.redraw(self)

    def update(self, events):
        for event in events:
            if event.type == Event.Type.KeyPressed:
                if event.data == Event.Key.K_ESCAPE:
                    self.parent.pause_game()
                    return
                if event.data in GameForm.KEYS:
                    self.game.snake_mind.desire(GameForm.KEYS[event.data])
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            self.parent.open_main_menu()
            return
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
    playing = True
    while playing:
        events = gui.check_events()
        for event in events:
            if event.type == Event.Type.Quit:
                playing = False
        
        main_window.layout.update(events)
        gui.update()
        time.sleep(1.0/main_window.fps)
