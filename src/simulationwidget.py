from tkinter import Frame, Button
from aiview import AIView
from aiscene import AIScene
from game import Game


class SimulationWidget(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self._running = False

        control_frame = Frame(self)
        self._button = Button(
            master=control_frame,
            text="Start simutation",
            command=self._start,
        )
        self._button.pack(side='left')

        Button(control_frame, text="Import").pack(side='left')
        Button(control_frame, text="Export").pack(side='left')
        control_frame.pack()

        self._controller = controller
        self._game = Game()
        self._game_scene = AIScene(self)
        self._game_scene.draw(self._game)
        self._game_scene.pack(fill='both', expand=True)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.pack(fill='both', expand=True)

    def set_controller(self, controller):
        simulation_state = self._running
        self._stop()

        self._controller = controller
        self._ai_view.set_contorller(controller)
        self.reset()

        if simulation_state:
            self._start()

    def update(self):
        if not self._running:
            return

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
        self._stop()
        self._game.restart()
        self._game_scene.clear()
        self._game_scene.draw(self._game)

    def _start(self):
        self._button.configure(
            text="Stop simulation",
            command=self._stop
        )
        self._running = True

    def _stop(self):
        self._button.configure(
            text="Start simulation",
            command=self._start
        )
        self._running = False
