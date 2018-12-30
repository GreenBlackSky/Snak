from widgets import Window, Layout
from gamescene import GameScene


class MainWindow(Window):
    def __init__(self, gui, config):
        super().__init__(None, gui, config)
        self.config = config
        self.layouts = {
            "MainMenu": Layout(self, gui, self.config["MainMenu"]),
            "PauseMenu": Layout(self, gui, self.config["PauseMenu"]),
            "EvolutionMenu": Layout(self, gui, self.config["EvolutionMenu"]),
            "Game": GameScene(self, gui, self.config["GameScene"])
        }
        self.layout = self.layouts["MainMenu"]
        self.fps = config["fps"]
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