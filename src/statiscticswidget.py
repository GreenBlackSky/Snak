"""Module contains StatisticsWidget class."""

from tkinter import Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatisticsWidget(Frame):
    """Widget can display given data."""
    def __init__(self, master):
        Frame.__init__(self, master)

        self._generation_count = 0

        fig = Figure(figsize=(5, 4), dpi=100)
        self._axes = fig.add_subplot(111)

        self._axes.set_facecolor('#000000')

        self._canvas = FigureCanvasTkAgg(fig, master=self)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(
            side='top',
            fill='both',
            expand=True
        )

    def reset(self):
        """Reset widget."""
        self._axes.clear()
        self._canvas.draw()

    def set_data_callback(self, event):
        """Add scores from event to displayed statistics."""
        data = event.widget.data
        self._generation_count += 1
        for gen_n, spec_id, score in data:
            self._axes.plot(self._generation_count, score, 'sy')
        self._canvas.draw()
