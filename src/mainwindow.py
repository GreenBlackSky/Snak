"""Module contains MainWindow of app."""

from MWidgets import Window


class MainWindow(Window):
    """Main window of application."""

    def __init__(self, gui, layout_name=None):
        """Create new MainWindow with name of initial top layout."""
        super().__init__(gui)
        self.layouts = dict()
        self.default_layout_name = layout_name
        self.triggers = {
            **self.triggers,
            "pause_game": self.pause_game,
            "continue_game": self.continue_game,
            "open_main_menu": self.open_main_menu,
            "open_evolution_menu": self.open_evolution_menu,
            "start_new_game": self.start_new_game
        }

    @classmethod
    def from_config(cls, config, gui):
        """Load window and its heirs from config."""
        ret = cls(gui, config["layout"])
        return ret

    def add_widget(self, widget, id):
        """Add child widget."""
        self.layouts[id] = widget
        if not self.widgets or id == self.default_layout_name:
            super().add_widget(self.layouts[id])

    def pause_game(self):
        super().add_widget(self.layouts["pause_menu"])

    def continue_game(self):
        super().add_widget(self.layouts["game_scene"])

    def open_main_menu(self):
        super().add_widget(self.layouts["main_menu"])

    def open_evolution_menu(self):
        super().add_widget(self.layouts["evolution_menu"])

    def start_new_game(self):
        super().add_widget(self.layouts["game_scene"])

# TODO Implement switching between layouts without additional methods
