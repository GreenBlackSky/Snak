"""MainMenuFrame class."""

from tkinter import Frame, Button, Listbox, BOTH


class MainMenuFrame(Frame):
    """Frame contains buttons to new game and options, and record table."""

    def __init__(self, app):
        """Create MainMenuFrame."""
        super().__init__(app)

        Button(
            self,
            text="Play game",
            command=self.master.game
        ).pack(fill=BOTH, expand=True)

        Button(
            self,
            text="A.I.",
            command=self.master.ai
        ).pack(fill=BOTH, expand=True)

        Button(
            self,
            text="Quit",
            command=self.master.destroy
        ).pack(fill=BOTH, expand=True)
