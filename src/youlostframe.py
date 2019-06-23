from tkinter import Frame, Label, Button


class YouLostFrame(Frame):
    def __init__(self, master, score):
        super().__init__(master)
        Label(self, text="You just lost.").pack()
        Label(self, text="Youre score:").pack()
        Label(self, textvar=score).pack()
        Button(self, text="Play again", command=self.master.game).pack()
        Button(self, text="Menu", command=self.master.main_menu).pack()
