from gui import GUI
from gamescene import GameScene
from mwidgets import Window, Loader, Widget


class MainWindow(Window):
    def __init__(self, config, _):
        Loader.register_widget("GameScene", GameScene)
        *_, w, h = config["rect"]
        super().__init__(config, gui=GUI(w, h))
        self.highscore = 0
        self.triggers = {
            **self.triggers,
            "pause_game": self.pause_game,
            "continue_game": self.continue_game,
            "open_main_menu": self.open_main_menu,
            "open_evolution_menu": self.open_evolution_menu,
            "start_new_game": self.start_new_game
        }

    def pause_game(self):
        self.layout = self.children["pause_menu"]

    def continue_game(self):
        self.layout = self.children["game_scene"]

    def open_main_menu(self):
        self.layout = self.children["main_menu"]

    def open_evolution_menu(self):
        self.layout = self.children["evolution_menu"]

    def start_new_game(self):
        self.layout = self.children["game_scene"]
        self.layout.reset()

# TODO Move gui to main.py