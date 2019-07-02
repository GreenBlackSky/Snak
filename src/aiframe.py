"""AIFrame class."""

from tkinter import Frame, Button, Listbox
from aicontroller import AIController
from aiview import AIView
from game import Game
from gamescene import GameScene
from config import STEP


class AIFrame(Frame):
    def __init__(self, master, **kargs):
        super().__init__(master, **kargs)
        self._controller = AIController()

        Button(
            self,
            text="Menu",
            command=self.master.main_menu,
            takefocus=False
        ).grid()

        self._ai_list_box = Listbox(self)
        self._ai_list_box.grid(row=1, rowspan=2, sticky='NSWE')

        self._game = Game()
        self._game_scene = GameScene(self)
        self._game_scene.grid(column=1, row=1)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.grid(column=1, row=2)

        self._run = False
        self.update()

    def update(self):
        """Update GameScene.

        Schedules call of itself.
        """
        if not self._run:
            self.after(STEP, self.update)
            return

        if self._game.is_lost():
            self._game.restart()
            self._game_scene.clear()
            self._game_scene.draw(self._game)
            self.after(STEP, self.update)
            return

        self._controller.update()
        self._ai_view.update()
        self._game.update(self._controller.direction)
        self._game_scene.redraw(self._game)
        self.after(STEP, self.update)

    def pack(self, *args, **kargs):
        self._game_scene.draw(self._game)
        self._run = True
        Frame.pack(self, *args, **kargs)

    def pack_forget(self, *args, **kargs):
        self._game.restart()
        self._game_scene.clear()
        self._run = False
        Frame.pack_forget(self, *args, **kargs)
