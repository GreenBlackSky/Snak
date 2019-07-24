"""Module contains the AIFrame class."""

from tkinter import Frame, Button
from evolutionwidget import EvolutionWidget
from simulationwidget import SimulationWidget
from config import STEP


class AIFrame(Frame):
    """
    Frame with some widgets to perform the evolution of the ai.

    Allows user to observe the ai behavement during its development.
    """

    def __init__(self, master, **kargs):
        """Create the AIFrame."""
        super().__init__(master, **kargs)

        self._exiting = False

        Button(
            master=self,
            text='Menu',
            command=self._signal_to_exit,
        ).grid()

        self._evolution = EvolutionWidget(self)
        self._evolution.bind(
            "<<TreeviewSelect>>",
            self._switch_displayed_controller
        )
        self._evolution.grid(row=1, sticky='ns')

        self._simulation = SimulationWidget(
            master=self,
            controller=self._evolution.selected_controller()
        )
        self._simulation.grid(column=1, row=0, rowspan=2)

        self.update()

    def update(self):
        """Update widgets.

        Schedules call of itself.
        """
        self._simulation.update()
        self._evolution.update()
        if self._exiting and not self._evolution.running:
            self.master.main_menu()

        self.after(STEP, self.update)

    def pack_forget(self, *args, **kargs):
        """
        Remove the frame from the masters space.

        Overloaded to stop all processes while the frame is not visible.
        """
        self._simulation.reset()
        self._evolution.reset()
        self._exiting = False
        Frame.pack_forget(self, *args, **kargs)

    def _switch_displayed_controller(self, _):
        controller = self._evolution.selected_controller()
        self._simulation.set_controller(controller)

    def _signal_to_exit(self):
        self._evolution.signal_to_stop()
        self._exiting = True
