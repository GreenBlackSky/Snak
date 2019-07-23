from tkinter import Frame
from aiview import AIView
from aiscene import AIScene
from game import Game


class SimulationWidget(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self._controller = controller
        self._game = Game()
        self._game_scene = AIScene(self)
        self._game_scene.draw(self._game)
        self._game_scene.pack(fill='both', expand=True)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.pack(fill='both', expand=True)

    def set_controller(self, controller):
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self.reset()

    def update(self):
        self._game.update(self._controller.direction)
        self._controller.percive(self._game)
        if self._game.is_lost:
            self._controller.reset()
            self.reset()
        else:
            self._ai_view.update()
            self._game_scene.redraw(self._game, self._controller)
            self._controller.update()

    def reset(self):
        self._game.restart()
        self._game_scene.clear()
        self._game_scene.draw(self._game)
