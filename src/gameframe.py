"""GameFrame class."""

from tkinter import Frame, Label, Button
from gamescene import GameScene


class GameFrame(Frame):
    """Frame contains game field to play on."""

    def __init__(self, app, score):
        """Create GameFrame."""
        super().__init__(app)
        self._score = score
        self._score.set('0')
        Label(self, text='Score:').grid(column=0, row=0)
        Label(self, textvar=self._score).grid(column=1, row=0)

        Button(
            self,
            text="Menu",
            command=self.master.main_menu,
            takefocus=False
        ).grid(column=2, row=0)

        self._game_scene = GameScene(self)
        self._game_scene.grid(column=0, columnspan=3, row=1)
        self._game_scene.focus_force()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score.set(str(val))

    def pack(self, *args, **kargs):
        self._game_scene.run = True
        Frame.pack(self, *args, **kargs)

    def pack_forget(self, *args, **kargs):
        self._game_scene.restart_game()
        Frame.pack_forget(self, *args, **kargs)
