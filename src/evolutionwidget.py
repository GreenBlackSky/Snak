"""Module contains the EvolutionWidget class."""

from tkinter.ttk import Treeview
from tkinter import Frame, Scrollbar, Button
from aipool import AIPool


class EvolutionWidget(Frame):
    """
    List-based widget, purpoced to control evolution.

    By pressing the button, user can start and stop evolution
    of controllers. Picking controller from list leads to
    generating <<SelectController>> event.
    """

    def __init__(self, master):
        """Create EvolutionWidget."""
        Frame.__init__(self, master)

        self._running = False
        self._stoping = False

        self._button = Button(
            master=self,
            text='Start evolution',
            command=self._start,
        )
        self._button.pack()

        self._pool = AIPool()

        columns = ("Gen", "Id", "Score")
        self._list = Treeview(
            master=self,
            selectmode='browse',
            columns=columns,
            show='headings'
        )
        self._list.bind(
            "<<TreeviewSelect>>",
            self._pass_controller
        )

        for column_id in columns:
            self._list.column(column_id, width=50)
            self._list.heading(column_id, text=column_id)
        self._list.pack(side='left', fill='both')

        scrollbar = Scrollbar(
            master=self,
            orient='vertical',
            command=self._list.yview
        )
        scrollbar.pack(side='left', fill='y')
        self._list.configure(yscrollcommand=scrollbar.set)

        self._list.selection_set(self._list.identify_row(0))
        self._update_data()

    def update(self):
        """
        Update widget.

        Widget makes calculations in separate process.
        If calculations for current generation are finished,
        this method updates list. Does nothing otherwise.
        """
        if self._running and self._pool.ready:
            self._update_data()

            if self._stoping:
                self._stop()

            if self._running:
                self._pool.process_generation()

    def selected_controller(self):
        """Get currently selected controller."""
        selected_item_id = self._list.selection()
        if not selected_item_id:
            selected_item_id = self._list.identify_row(0)
        selected_item = self._list.item(selected_item_id)
        controller_id = tuple(selected_item['values'])
        return self._pool.get_instance_by_id(controller_id[:-1])

    def reset(self):
        """Reset widget to default state."""
        self._stop()
        self._pool = AIPool()
        self._update_data()

    def signal_to_stop(self):
        """
        Send widget signal to stop.

        Widget would stop evolution after calculations for
        current generations are over.
        """
        self._stoping = True
        self._button.configure(state='disable')

    @property
    def running(self):
        """Check if calculations for current generationl are over."""
        return self._running

    def _start(self):
        self._button.configure(
            text="Stop evolution",
            command=self.signal_to_stop
        )
        self._running = True

    def _stop(self):
        self._button.configure(
            text="Start evolution",
            command=self._start,
            state='normal'
        )
        self._stoping = False
        self._running = False

    def _update_data(self):
        for child in self._list.get_children():
            self._list.delete(child)
        for (gen, spec_id, score) in self._pool.get_instances_data():
            self._list.insert('', 'end', values=(gen, spec_id, score))

    def _pass_controller(self, event):
        self.event_generate("<<SelectController>>")
