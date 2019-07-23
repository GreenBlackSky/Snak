
from tkinter import Frame, Button


class ControlWidget(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self._run_simulation = False
        self._run_evolution = False
        self._stoping_evolution = False
        self._exiting = False

        Button(
            master=self,
            text="Menu",
            command=self._signal_to_exit,
        ).pack(side='left')

        self._evolution_button = Button(
            master=self,
            text='Start evolution',
            command=self.start_evolution,
        )
        self._evolution_button.pack(side='left')

        Button(
            master=self,
            text='Mode:Simulation'
        ).pack(side='left')

        self._simulation_button = Button(
            master=self,
            text="Start simutation",
            command=self.start_simulation,
        )
        self._simulation_button.pack(side='left')

        Button(
            master=self,
            text='Import NN'
        ).pack(side='left')

        Button(
            master=self,
            text='Export NN'
        ).pack(side='left')

    def reset(self):
        self._run_simulation = False
        self._run_evolution = False
        self._stoping_evolution = False
        self._exiting = False

    def start_simulation(self):
        self._simulation_button.configure(
            text="Stop simulation",
            command=self.stop_simulation
        )
        self._run_simulation = True

    def stop_simulation(self):
        self._simulation_button.configure(
            text="Start simulation",
            command=self.start_simulation
        )
        self._run_simulation = False

    def start_evolution(self):
        self._evolution_button.configure(
            text="Stop evolution",
            command=self._signal_to_stop_evolution
        )
        self._run_evolution = True

    def _signal_to_stop_evolution(self):
        self._stoping_evolution = True
        self._evolution_button.configure(state='disable')

    def stop_evolution(self):
        self._evolution_button.configure(
            text="Start evolution",
            command=self.start_evolution,
            state='normal'
        )
        self._stoping_evolution = False
        self._run_evolution = False

    def _signal_to_exit(self):
        self._signal_to_stop_evolution()
        self._exiting = True

    @property
    def run_evolution(self):
        return self._run_evolution

    @property
    def run_simulation(self):
        return self._run_simulation

    @property
    def stoping_evolution(self):
        return self._stoping_evolution

    @property
    def exiting(self):
        return self._exiting
