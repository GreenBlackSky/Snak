from basecontroller import BaseController


class TkController(BaseController):
    def __init__(self, master):
        BaseController.__init__(self)
        master.bind("<Key-Up>", lambda event: self.move_up())
        master.bind("<Key-Down>", lambda event: self.move_down())
        master.bind("<Key-Left>", lambda event: self.move_left())
        master.bind("<Key-Right>", lambda event: self.move_right())
