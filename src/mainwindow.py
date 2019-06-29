"""MainWindow class."""

from tkinter import Tk, BOTH

from tkcontroller import TkController
from aicontroller import AIController
from mainmenuframe import MainMenuFrame
from gameframe import GameFrame
from aiframe import AIFrame
from youlostframe import YouLostFrame


class MainWindow(Tk):
    """MainWindow contains all widgets in app."""

    def __init__(self):
        """Create MainWindow."""
        super().__init__()

        self.title("Snak")
        self._main_window_frame = MainMenuFrame(self)
        self._game_frame = GameFrame(self, TkController(self))
        self._ai_frame = AIFrame(self, AIController())
        self._you_lost_frame = YouLostFrame(self)

        self.main_menu()

    def main_menu(self):
        """Set MainMenuFrame on top of app."""
        for widget in self.pack_slaves():
            widget.pack_forget()
        self._main_window_frame.pack(fill=BOTH, expand=True)

    def game(self):
        """Set GameFrame on top of app."""
        for widget in self.pack_slaves():
            widget.pack_forget()
        self._game_frame.pack(fill=BOTH, expand=True)

    def ai(self):
        """Set AIFrame on top of app."""
        for widget in self.pack_slaves():
            widget.pack_forget()
        self._ai_frame.pack(fill=BOTH, expand=True)

    def you_lost(self, score):
        """Set YouLostFrame on top of app."""
        for widget in self.pack_slaves():
            widget.pack_forget()
        self._you_lost_frame.set_score(score)
        self._you_lost_frame.pack(fill=BOTH, expand=True)
