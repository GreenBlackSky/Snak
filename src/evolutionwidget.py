from tkinter.ttk import Treeview
from tkinter import Frame, Scrollbar
from aipool import AIPool


class EvolutionWidget(Frame):

    def __init__(self, master):
        self._pool = AIPool()
        columns = ("Gen", "Id", "Score")
        Frame.__init__(self, master)
        self._list = Treeview(
            self,
            selectmode='browse',
            columns=columns,
            show='headings'
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
        self.update()

    def update(self):
        for child in self._list.get_children():
            self._list.delete(child)
        for (gen, spec_id, score) in self._pool.get_instances_data():
            self._list.insert('', 'end', values=(gen, spec_id, score))

    def bind(self, *args):
        self._list.bind(*args)

    def selected_controller(self):
        selected_item_id = self._list.selection()
        if not selected_item_id:
            selected_item_id = self._list.identify_row(0)
        selected_item = self._list.item(selected_item_id)
        controller_id = tuple(selected_item['values'])
        return self._pool.get_instance_by_id(controller_id[:-1])

    @property
    def ready(self):
        return self._pool.ready

    def process_generation(self):
        self._pool.process_generation()
