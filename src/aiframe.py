"""Module contains the AIFrame class."""

from tkinter import Frame
from evolutionwidget import EvolutionWidget
from controlwidget import ControlWidget
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

        self._control = ControlWidget(self)
        self._control.pack(fill='x')

        self._evolution = EvolutionWidget(self)
        self._evolution.pack(side='left', fill='both')
        self._evolution.bind(
            "<<TreeviewSelect>>",
            self._switch_displayed_controller
        )

        self._simulation = SimulationWidget(
            master=self,
            controller=self._evolution.selected_controller()
        )
        self._simulation.pack(side='left', fill='both', expand=True)

        self.update()

    def update(self):
        """Update widgets.

        Schedules call of itself.
        """
        if self._control.run_simulation:
            self._simulation.update()

        if self._control.run_evolution and self._evolution.ready:
            self._evolution.update()

            if self._control.stoping_evolution:
                self._control.stop_evolution()

            if self._control.run_evolution:
                self._evolution.process_generation()

        if self._control.exiting and not self._control.run_evolution:
            self.master.main_menu()

        self.after(STEP, self.update)

    def pack_forget(self, *args, **kargs):
        """
        Remove the frame from the masters space.

        Overloaded to stop all processes while the frame is not visible.
        """
        self._control.reset()
        self._simulation.reset()
        self._evolution.reset()
        self._control.stop_evolution()
        self._control.stop_simulation()
        Frame.pack_forget(self, *args, **kargs)

    def _switch_displayed_controller(self, _):
        simulation_state = self._control.run_simulation
        self._control.stop_simulation()

        controller = self._evolution.selected_controller()
        self._simulation.set_controller(controller)

        if simulation_state:
            self._control.start_simulation()
