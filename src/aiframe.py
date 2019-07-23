"""Module contains the AIFrame class."""

from tkinter import Frame
from evolutionwidget import EvolutionWidget
from controlwidget import ControlWidget
from aiview import AIView
from aiscene import AIScene
from game import Game
from config import STEP


class AIFrame(Frame):
    """
    Frame with some widgets to perform the evolution of the ai.

    Allows user to observe the ai behavement during its development.
    """

    def __init__(self, master, **kargs):
        """Create the AIFrame."""
        super().__init__(master, **kargs)

        self._control = ControlWidget(self)
        self._control.pack(fill='x')

        self._evolution = EvolutionWidget(self)
        self._evolution.pack(side='left', fill='both')
        self._evolution.bind(
            "<<TreeviewSelect>>",
            self._switch_displayed_controller
        )

        self._controller = self._evolution.selected_controller()

        self._game = Game()
        self._game_scene = AIScene(self)
        self._game_scene.draw(self._game)
        self._game_scene.pack(fill='both', expand=True)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.pack(fill='both', expand=True)

        self.update()

    def update(self):
        """Update widgets.

        Schedules call of itself.
        """
        if self._control.run_simulation:
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

        if self._control.run_evolution and self._evolution.ready:
            self._evolution.update()

            if self._control.stoping_evolution:
                self._control.stop_evolution()

            if self._control.run_evolution:
                self._evolution.process_generation()

        self.after(STEP, self.update)

    def pack_forget(self, *args, **kargs):
        """
        Remove the frame from the masters space.

        Overloaded to stop all processes while the frame is not visible.
        """
        self._game.restart()
        self._game_scene.clear()
        self._control.stop_evolution()
        self._control.stop_simulation()
        Frame.pack_forget(self, *args, **kargs)

    def _switch_displayed_controller(self, _):
        controller = self._evolution.selected_controller()

        simulation_state = self._control.run_simulation
        self._control.stop_simulation()
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self._game.restart()
        self._game_scene.draw(self._game)

        if simulation_state:
            self._control.start_simulation()
