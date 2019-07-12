"""Module contains AIFrame class."""

from tkinter import Frame, Button, Listbox
from aipool import AIPool
from aiview import AIView
from aiscene import AIScene
from game import Game
from config import STEP


class AIFrame(Frame):
    """Frame with some widgets to perform and observe evolution of ai."""

    def __init__(self, master, **kargs):
        """Create AIFrame."""
        super().__init__(master, **kargs)
        self._pool = AIPool()

        Button(
            self,
            text="Menu",
            command=self.master.main_menu,
            takefocus=False
        ).pack()

        self._ai_list_box = Listbox(self, selectmode='single')
        self._ai_list_box.pack(side='left', fill='both')
        self._ai_list_box.insert(0, *self._pool.get_instances_ids())
        self._ai_list_box.bind(
            "<<ListboxSelect>>",
            self._switch_displayed_nn
        )
        self._ai_list_box.selection_set(0)

        self._controller = self._pool.get_instance_by_id(0)

        self._game = Game()
        self._game_scene = AIScene(self)
        self._game_scene.pack(fill='both', expand=True)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.pack(fill='both', expand=True)

        self._run = False
        self.update()

    def update(self):
        """Update GameScene.

        Schedules call of itself.
        """
        if not self._run:
            self.after(STEP, self.update)
            return

        self._game.update(self._controller.direction)
        self._controller.percive(self._game)
        if self._game.is_lost:
            self._controller.reset()
            self._game.restart()
            self._game_scene.clear()
            self._game_scene.draw(self._game)
        else:
            self._ai_view.update()
            self._game_scene.redraw(self._game, self._controller)
            self._controller.update()
        self.after(STEP, self.update)

    def _switch_displayed_nn(self, *_):
        nn_n = self._ai_list_box.get(self._ai_list_box.curselection()[0])
        controller = self._pool.get_instance_by_id(nn_n)
        self._run = False
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self._game.restart()
        self._game_scene.draw(self._game)
        self._run = True

    def pack(self, *args, **kargs):
        """
        Pack frame into master space.

        Overloaded to start all processes when frame is visible.
        """
        self._game_scene.draw(self._game)
        self._run = True
        Frame.pack(self, *args, **kargs)

    def pack_forget(self, *args, **kargs):
        """
        Remove frame from masters space.

        Overloaded to stop all processes while frame is not visible.
        """
        self._game.restart()
        self._game_scene.clear()
        self._run = False
        Frame.pack_forget(self, *args, **kargs)
