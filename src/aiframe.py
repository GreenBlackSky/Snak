"""AIFrame class."""

from tkinter import Frame, Label, Button, Canvas
from gamescene import GameScene


class AIFrame(Frame):
    """Contains widgets to tune game."""

    def __init__(self, app):
        """Create AIFrame."""
        super().__init__(app)
        self._game_scene = GameScene(self, 10)
        # self._game_scene.grid(column=0, row=0)
        self._game_scene.pack()
        # Canvas(self, background="white").grid(column=1, row=0)
        Button(
            self,
            text="Menu",
            command=self.master.main_menu
        ).pack()

    def pack(self, *args, **kargs):
        self._game_scene.run = True
        Frame.pack(self, *args, **kargs)

    def pack_forget(self, *args, **kargs):
        self._game_scene.restart_game()
        Frame.pack_forget(self, *args, **kargs)
