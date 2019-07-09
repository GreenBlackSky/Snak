from tkinter import Canvas


class AIView(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master, background='white')
        self._controller = None
        self._nodes = {}
        self._connectors = {}

    def set_contorller(self, controller):
        self._controller = controller
        self._nodes = {}
        self._connectors = {}
        scheme = self._controller.scheme
        cell_width = int(self['width'])//len(scheme)
        cell_height = int(self['height'])//max(scheme)
        R = min(cell_width, cell_height)//3
        self._draw_connectors(cell_width, cell_height, R)
        self._draw_nodes(cell_width, cell_height, R)

    def update(self):
        max_min_scheme = self._controller.max_min()
        for (x, y), node in self._nodes.items():
            val = self._controller.get_node_value(x, y)
            color = self._get_color(val, *max_min_scheme[x])
            self.itemconfig(node, fill=color)

    def _get_color(self, val, max_lim, min_lim):
        if val < 0:
            shade = hex(int(255*val/min_lim))[2:]
            if len(shade) == 1:
                shade = '0' + shade
            color = f"#ff{shade}{shade}"
        elif val > 0:
            shade = hex(int(255*val/max_lim))[2:]
            if len(shade) == 1:
                shade = '0' + shade
            color = f"#{shade}ff{shade}"
        else:
            color = "#ffffff"
        return color

    def _draw_nodes(self, cell_width, cell_height, R):
        for x, layer in enumerate(self._controller.scheme):
            for y in range(layer):
                xc = int(cell_width*(x + 0.5))
                yc = int(cell_height*(y + 0.5))
                self._nodes[(x, y)] = self.create_oval(
                    xc - R, yc - R, xc + R, yc + R
                )

    def _draw_connectors(self, cell_width, cell_height, R):
        scheme = self._controller.scheme
        for x2 in range(1, len(scheme)):
            x1 = x2 - 1
            for y2 in range(scheme[x2]):
                for y1 in range(scheme[x1]):
                    weight = self._controller.get_connection(
                        x1, y1, x2, y2
                    )
                    color = self._get_color(weight, 1, -1)
                    self._connectors[((x1, y1), (x2, y2))] = self.create_line(
                        int(cell_width*(x1 + 0.5)) + R,
                        int(cell_height*(y1 + 0.5)),
                        int(cell_width*(x2 + 0.5)) - R,
                        int(cell_height*(y2 + 0.5)),
                        width=2,
                        fill=color
                    )
