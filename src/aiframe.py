"""Module contains the AIFrame class."""

from tkinter import Frame, Scrollbar
from tkinter.ttk import Treeview
from aicontrol import AIControl
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

        self._control = AIControl(self)
        self._control.pack(fill='x')

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

        if self._control.run_evolution and self._pool.ready:
            for child in self._ai_list.get_children():
                self._ai_list.delete(child)
            for (gen, spec_id, score) in self._pool.get_instances_data():
                self._ai_list.insert('', 'end', values=(gen, spec_id, score))
            self._ai_list.selection_set(self._ai_list.identify_row(0))

            if self._control.stoping_evolution:
                self._control.stop_evolution()

            if self._control.run_evolution:
                self._pool.process_generation()

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
        nn_n = tuple(self._ai_list.item(self._ai_list.focus())['values'])
        if not nn_n:
            return

        simulation_state = self._control.run_simulation
        self._control.stop_simulation()

        controller = self._pool.get_instance_by_id(nn_n[:-1])
        self._controller = controller
        self._ai_view.set_contorller(controller)
        self._game.restart()
        self._game_scene.draw(self._game)

        if simulation_state:
            self._control.start_simulation()

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
