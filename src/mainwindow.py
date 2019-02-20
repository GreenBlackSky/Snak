"""Module contains MainWindow of app."""

from MWidgets import Window


class MainWindow(Window):
    """Main window of application."""

    def __init__(self, rect, fps=None, layout_name=None):
        """Create new MainWindow with fps and name of initial top layout."""
        super().__init__(rect, fps, layout_name)
        self.triggers = {**self.triggers,
                         "pause_game": self.pause_game,
                         "continue_game": self.continue_game,
                         "open_main_menu": self.open_main_menu,
                         "open_evolution_menu": self.open_evolution_menu,
                         "start_new_game": self.start_new_game
                         }

    def pause_game(self):
        self.set_layout("pause_menu")

    def continue_game(self):
        self.set_layout("game_scene")

    def open_main_menu(self):
        self.set_layout("main_menu")

    def open_evolution_menu(self):
        self.set_layout("evolution_menu")

    def start_new_game(self):
        self.set_layout("game_scene")
