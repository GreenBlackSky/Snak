from tkinter import Canvas


class ResizibleCanvas(Canvas):
    def __init__(self, master, **kargs):
        Canvas.__init__(self, master, **kargs)
        self._width = self.winfo_reqwidth()
        self._height = self.winfo_reqheight()
        self.bind('<Configure>', self._on_resize)

    def _on_resize(self, event):
        wscale = event.width/self._width
        hscale = event.height/self._height
        self._width = event.width
        self._height = event.height
        self.scale('all', 0, 0, wscale, hscale)
