"""Module contains the AIFrame class."""

from tkinter import Frame, Button, Listbox, Scrollbar
from aipool import AIPool
from aiview import AIView
from aiscene import AIScene
from game import Game
from config import STEP


class AIFrame(Frame):
    """
    Frame with some widgets to perform and observe the evolution of the ai.
    """

    def __init__(self, master, **kargs):
        """Create the AIFrame."""
        super().__init__(master, **kargs)

        control_frame = Frame(self)
        Button(
            master=control_frame,
            text="Menu",
            command=self.master.main_menu,
        ).pack(side='left')

        self._evolution_button = Button(
            master=control_frame,
            text='Start evolution',
            command=self._start_evolution,
        )
        self._evolution_button.pack(side='left')

        self._simulation_button = Button(
            master=control_frame,
            text="Start simutation",
            command=self._start_simulation,
        )
        self._simulation_button.pack(side='left')

        Button(
            master=control_frame,
            text='Import NN'
        ).pack(side='left')

        Button(
            master=control_frame,
            text='Export NN'
        ).pack(side='left')

        control_frame.pack(fill='x')

        self._pool = AIPool()
        self._ai_listbox = Listbox(self, selectmode='single')
        self._ai_listbox.pack(side='left', fill='both')
        self._ai_listbox.bind(
            "<<ListboxSelect>>",
            self._switch_displayed_controller
        )
        scrollbar = Scrollbar(
            master=self,
            orient='vertical',
            command=self._ai_listbox.yview
        )
        scrollbar.pack(side='left', fill='y')
        self._ai_listbox.configure(yscrollcommand=scrollbar.set)

        self._ai_listbox.insert(0, *self._pool.get_instances_ids())
        self._ai_listbox.selection_set(0)
        self._controller = self._pool.get_instance_by_id((0, 0))

        self._game = Game()
        self._game_scene = AIScene(self)
        self._game_scene.draw(self._game)
        self._game_scene.pack(fill='both', expand=True)

        self._ai_view = AIView(self)
        self._ai_view.set_contorller(self._controller)
        self._ai_view.pack(fill='both', expand=True)

        self._run_simulation = False
        self._run_evolution = False
        self._stoping_evolution = False
        self.update()

    def update(self):
        """Update widgets.

        Schedules call of itself.
        """
        if self._run_simulation:
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

        if self._stoping_evolution and self._pool.ready():
            self._ai_listbox.delete(0, 'end')
            self._ai_listbox.insert(0, *self._pool.get_instances_ids())
            self._stoping_evolution = False

        if self._run_evolution and self._pool.ready():
            self._ai_listbox.delete(0, 'end')
            self._ai_listbox.insert(0, *self._pool.get_instances_ids())
            self._pool.start_process()

        self.after(STEP, self.update)

    def pack_forget(self, *args, **kargs):
        """
        Remove the frame from the masters space.

        Overloaded to stop all processes while the frame is not visible.
        """
        self._game.restart()
        self._game_scene.clear()
        self._stop_evolution()
        self._stop_simulation()
        Frame.pack_forget(self, *args, **kargs)

    def _start_simulation(self):
        self._simulation_button.configure(
            text="Stop simulation",
            command=self._stop_simulation
        )
        self._run_simulation = True

    def _stop_simulation(self):
        self._simulation_button.configure(
            text="Start simulation",
            command=self._start_simulation
        )
        self._run_simulation = False

    def _start_evolution(self):
        self._evolution_button.configure(
            text="Stop evolution",
            command=self._stop_evolution
        )
        self._run_evolution = True

    def _stop_evolution(self):
        self._evolution_button.configure(
            text="Start evolution",
            command=self._start_evolution
        )
        self._run_evolution = False
        self._stoping_evolution = True

    def _switch_displayed_controller(self, _):
        nn_n = self._ai_listbox.get(self._ai_listbox.curselection()[0])
        controller = self._pool.get_instance_by_id(nn_n)
        simulation_state, self._run_simulation = self._run_simulation, False
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self._game.restart()
        self._game_scene.draw(self._game)
        self._run_simulation = simulation_state
