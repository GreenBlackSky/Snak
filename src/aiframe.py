"""Module contains the AIFrame class."""

from tkinter import Frame, Button
from tkinter.ttk import Notebook
from evolutionwidget import EvolutionWidget
from simulationwidget import SimulationWidget
from statiscticswidget import StatisticsWidget
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

        column_1 = Frame(self)
        column_1.pack(side='left', fill='y', expand=False)

        Button(
            master=column_1,
            text='Menu',
            command=self._signal_to_exit,
        ).pack(fill='x', expand=False)

        self._evolution = EvolutionWidget(column_1)
        self._evolution.pack(fill='both', expand=True)

        notebook = Notebook(self)
        notebook.pack(side='left', fill='both', expand=True)

        self._simulation = SimulationWidget(
            master=notebook,
            controller=self._evolution.selected_controller()
        )
        self._evolution.bind(
            "<<SelectController>>",
            self._simulation.set_controller_callback
        )
        notebook.bind("<<NotebookTabChanged>>", self._simulation.stop)
        notebook.add(self._simulation, text="Simulation")

        self._statistics = StatisticsWidget(self)
        self._evolution.bind(
            "<<Updated>>",
            self._statistics.set_data_callback
        )
        notebook.add(self._statistics, text='Statistics')

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
        self._simulation.stop()
        self._simulation.reset()
        self._statistics.reset()
        self._evolution.reset()
        self._exiting = False
        Frame.pack_forget(self, *args, **kargs)

    def _signal_to_exit(self):
        self._evolution.signal_to_stop()
        self._exiting = True
