"""GameFrame class."""

from tkinter import Frame, Label, Button, StringVar
from game import Game
from gamescene import GameScene
from config import STEP


class GameFrame(Frame):
    """Frame contains game field to play on."""

    def __init__(self, app, controller, **kargs):
        """Create GameFrame."""
        super().__init__(app)

        self._controller = controller

        Button(
            self,
            text="Menu",
            command=self.master.main_menu,
            takefocus=False
        ).grid(column=0, row=0)

        self._score = StringVar()
        self._score.set('0')
        Label(self, text='Score:').grid(column=1, row=0)
        Label(self, textvar=self._score).grid(column=2, row=0)

        self._game = Game()
        self._game_scene = GameScene(self)
        self._game_scene.grid(column=0, columnspan=3, row=1)
        self._run = False
        self.update()

    def update(self):
        """Update GameScene.

        Schedules call of itself.
        """
        if not self._run:
            self.after(STEP, self.update)
            return

        self._controller.update()
        self._game.update(self._controller.direction)
        self._score.set(str(self._game.score))
        if self._game.is_lost:
            self.after(STEP, self.update)
            self.master.you_lost(self._game.score)
        else:
            self._game_scene.redraw(self._game)
            self.after(STEP, self.update)

    def pack(self, *args, **kargs):
        self._game_scene.draw(self._game)
        self._run = True
        Frame.pack(self, *args, **kargs)

    def pack_forget(self, *args, **kargs):
        self._game.restart()
        self._controller.move_up()
        self._game_scene.clear()
        self._run = False
        Frame.pack_forget(self, *args, **kargs)
