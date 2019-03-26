from mwidgets import Window, TabWidget


class MainWindow(Window):
    def __init__(self, gui):
        super().__init__(gui)
        self._widget = None
        TabWidget((0, 0, 1, 1), self)
        self._triggers = {
            **self._triggers,
            "pause_menu": lambda: self._widget.set_widget(0),
            "settings_menu": lambda: self._widget.set_widget(1),
            "evolution_menu": lambda: self._widget.set_widget(2),
            "game_scene": lambda: self._widget.set_widget(3),
            "main_menu": lambda: self._widget.set_widget(4)
        }

    def add_widget(self, widget):
        if self._widget:
            self._widget.add_widget(widget)
        else:
            self._widget = widget
