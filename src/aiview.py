from tkinter import Canvas


class AIView(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master, background='white')
        self._controller = None

    def set_contorller(self, controller):
        self._controller = controller
        self._nodes = {}
        self._connectors = {}
        scheme = self._controller.scheme
        cell_width = int(self['width'])//len(scheme)
        cell_height = int(self['height'])//max(scheme)
        R = min(cell_width, cell_height)//3
        self._draw_nodes(scheme, cell_width, cell_height, R)
        self._draw_connectors(scheme, cell_width, cell_height, R)

    def update(self):
        pass

    def _draw_nodes(self, scheme, cell_width, cell_height, R):
        for x, layer in enumerate(scheme):
            for y in range(layer):
                xc = int(cell_width*(x + 0.5))
                yc = int(cell_height*(y + 0.5))
                self._nodes[(x, y)] = self.create_oval(
                    xc - R, yc - R, xc + R, yc + R
                )

    def _draw_connectors(self, scheme, cell_width, cell_height, R):
        for x1 in range(len(scheme) - 1):
            x2 = x1 + 1
            for y1 in range(scheme[x1]):
                for y2 in range(scheme[x2]):
                    self._connectors[((x1, y1), (x2, y2))] = self.create_line(
                        int(cell_width*(x1 + 0.5)) + R,
                        int(cell_height*(y1 + 0.5)),
                        int(cell_width*(x2 + 0.5)) - R,
                        int(cell_height*(y2 + 0.5)),
                    )
