"""Module contains MainWindow of app."""

from mwidgets import Window


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
        def wrapper():
            self.set_layout(id)
        setattr(self, id, wrapper)

        self.layouts[id] = widget
        if not self.widgets or id == self.default_layout_name:
            super().add_widget(self.layouts[id])

    def set_layout(self, name):
        super().add_widget(self.layouts[name])

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

# TODO Implement switching between layouts without additional methods
