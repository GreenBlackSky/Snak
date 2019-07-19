"""Module contains the AIFrame class."""

from tkinter import Frame, Button, Listbox, Scrollbar
from tkinter.ttk import Treeview
from aipool import AIPool
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

        self._evolution_button = None
        self._simulation_button = None
        self._set_control_panel()

        self._controller = None
        self._pool = None
        self._ai_list = None
        self._set_listbox()

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

        if self._run_evolution and self._pool.ready():
            for child in self._ai_list.get_children():
                self._ai_list.delete(child)
            for (gen, spec_id, score) in self._pool.get_instances_data():
                self._ai_list.insert('', 'end', values=(gen, spec_id, score))
            self._ai_list.selection_set(self._ai_list.identify_row(0))

            if self._stoping_evolution:
                self._stoping_evolution = False
                self._stop_evolution()

            if self._run_evolution:
                self._pool.process_generation()

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

    def _set_control_panel(self):
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
            command=self._signal_to_stop_evolution
        )
        self._run_evolution = True

    def _signal_to_stop_evolution(self):
        self._stoping_evolution = True
        self._evolution_button.configure(state='disable')

    def _stop_evolution(self):
        self._evolution_button.configure(
            text="Start evolution",
            command=self._start_evolution,
            state='normal'
        )
        self._run_evolution = False

    def _switch_displayed_controller(self, _):
        nn_n = tuple(self._ai_list.item(self._ai_list.focus())['values'])
        if not nn_n:
            return
        controller = self._pool.get_instance_by_id(nn_n[:-1])
        simulation_state, self._run_simulation = self._run_simulation, False
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self._game.restart()
        self._game_scene.draw(self._game)
        self._run_simulation = simulation_state

    def _set_listbox(self):
        self._pool = AIPool()
        columns = ("Gen", "Id", "Score")
        self._ai_list = Treeview(
            self,
            selectmode='browse',
            columns=columns,
            show='headings'
        )
        for column_id in columns:
            self._ai_list.column(column_id, width=50)
            self._ai_list.heading(column_id, text=column_id)

        self._ai_list.pack(side='left', fill='both')
        self._ai_list.bind(
            "<<TreeviewSelect>>",
            self._switch_displayed_controller
        )

        scrollbar = Scrollbar(
            master=self,
            orient='vertical',
            command=self._ai_list.yview
        )
        scrollbar.pack(side='left', fill='y')
        self._ai_list.configure(yscrollcommand=scrollbar.set)

        for (gen, spec_id, score) in self._pool.get_instances_data():
            self._ai_list.insert('', 'end', values=(gen, spec_id, score))
        self._ai_list.selection_set(self._ai_list.identify_row(0))

        self._controller = self._pool.get_instance_by_id((0, 0))
