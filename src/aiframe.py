"""AIFrame class."""

from tkinter import Frame, Button, Canvas
from gamescene import GameScene
from game import Game
from aicontroller import AIController


class AIFrame(Frame):
    """Contains widgets to tune game."""

    def __init__(self, app):
        """Create AIFrame."""
        super().__init__(app)
        width = 20
        height = 10
        controller = AIController()
        game = Game(controller, width, height)
        self._game_scene = GameScene(self, game)
        self._game_scene.pack()
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
