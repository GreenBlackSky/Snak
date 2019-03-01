"""Module contains MainWindow of app."""

from mwidgets import Window


class MainWindow(Window):
    """Main window of application."""

    def __init__(self, gui):
        """Create new MainWindow with name of initial top layout."""
        super().__init__(gui)
        self.layouts = dict()

    def add_widget(self, widget, id):
        """Add child widget."""
        def wrapper():
            self.set_layout(id)

        self.triggers[id] = wrapper

        self.layouts[id] = widget
        super().add_widget(widget)

    def set_layout(self, name):
        """Display child layout with given name."""
        super().add_widget(self.layouts[name])
