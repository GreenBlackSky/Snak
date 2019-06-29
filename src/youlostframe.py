from tkinter import Frame, Label, Button


class YouLostFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="You just lost.").pack()
        Label(self, text="Youre score:").pack()
        self._score_label = Label(self)
        self._score_label.pack()
        Button(self, text="Play again", command=self.master.game).pack()
        Button(self, text="Menu", command=self.master.main_menu).pack()

    def set_score(self, score):
        self._score_label['text'] = str(score)
