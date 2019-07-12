"""Module contains YouLostFrame.

Basicly, it is a window, whish should be showed to user,
when he loses the game.
"""

from tkinter import Frame, Label, Button


class YouLostFrame(Frame):
    """
    You-just-lost-frame.

    Frame contains players final score and buttons,
    which leads player to main window or back to game.
    """

    def __init__(self, master):
        """Create YouLostFrame."""
        super().__init__(master)
        Label(self, text="You just lost.").pack(fill='both', expand=True)
        Label(self, text="Youre score:").pack(fill='both', expand=True)
        self._score_label = Label(self)
        self._score_label.pack(fill='both', expand=True)
        Button(
            self,
            text="Play again",
            command=self.master.game
        ).pack(fill='both', expand=True)
        Button(
            self,
            text="Menu",
            command=self.master.main_menu
        ).pack(fill='both', expand=True)

    def set_score(self, score):
        """Set displaying score."""
        self._score_label['text'] = str(score)
