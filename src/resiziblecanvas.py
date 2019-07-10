"""Module contains ResizibleCanvs widget."""

from tkinter import Canvas


class ResizibleCanvas(Canvas):
    """Canvas, which scales objects on it when is being resized."""
    def __init__(self, master, **kargs):
        Canvas.__init__(self, master, **kargs)
        self.bind('<Configure>', self._on_resize)
        self._width = self.winfo_reqwidth()
        self._height = self.winfo_reqheight()

    def _on_resize(self, event):
        wscale = float(event.width/self._width)
        hscale = float(event.height/self._height)
        self._width = event.width
        self._height = event.height
        # self.config(width=self._width, height=self._height)
        self.scale('all', 0, 0, wscale, hscale)
