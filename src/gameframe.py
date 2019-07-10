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

        self._score = StringVar()
        self._score.set('0')

        control_frame = Frame(self)
        Button(
            control_frame,
            text="Menu",
            command=self.master.main_menu,
            takefocus=False
        ).pack(side='left')
        Label(control_frame, text='Score:').pack(side='left')
        Label(control_frame, textvar=self._score).pack(side='left')
        control_frame.pack(fill='x')

        self._game = Game()
        self._game_scene = GameScene(self)
        self._game_scene.pack(fill='both', expand=True)
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
