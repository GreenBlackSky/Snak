from gamescene import GameScene
from mwidgets import Window, Layout, WidgetMaker

class MainWindow(Window):
    def __init__(self, config, gui):
        WidgetMaker.constructors["GameScene"] = GameScene
        super().__init__(config, gui=gui)
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
        self.layout = self.layouts["GameScene"]
        self.fps = 8

    def open_main_menu(self):
        self.fps = 20
        self.layout = self.layouts["MainMenu"]

    def open_evolution_menu(self):
        self.fps = 20
        self.layout = self.layouts["EvolutionMenu"]

    def start_new_game(self):
        self.layout = self.layouts["GameScene"]
        self.layout.reset()
        self.fps = 8