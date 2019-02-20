"""Module contains scene for playing Snak."""

from MWidgets import Scene, Widget, Event, Color, ColorRole
from game import Game


class GameScene(Scene):
    """Visual representation of game."""

    def __init__(self, rect, fps=None, cell_size=None, parent=None):
        """Create new scene with fps, cell size and parent."""
        super().__init__(rect, fps, cell_size, parent)
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score = None

        self.events = {
            **self.events,
            "Paused": Event.Type.Custom0,
            "Closed": Event.Type.Custom1
        }
        self.triggers = {**self.triggers,
                         "reset": self.reset,
                         "pause_game": self.pause_game,
                         "move_left": self.move_left,
                         "move_right": self.move_right,
                         "move_up": self.move_up,
                         "move_down": self.move_down}

    def add_child(self, id, child):
        """Override parents add_child to set score label."""
        super().add_child(id, child)
        if id == "score_label":
            self.score = child
            palette = self.score.palette[Widget.State.Active]
            palette[ColorRole.Foreground] = Color.BLACK
            palette[ColorRole.Text] = Color.DARK_GRAY

    def pause_game(self):
        self.emmit_event(Event.Type.Custom0)

    def move_left(self):
        self.game.snake_mind.desire((-1, 0))

    def move_right(self):
        self.game.snake_mind.desire((1, 0))

    def move_up(self):
        self.game.snake_mind.desire((0, -1))

    def move_down(self):
        self.game.snake_mind.desire((0, 1))

    def update(self, events):
        """Update situation in game."""
        super().update(events)
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            self.emmit_event(Event.Type.Custom1)

    def redraw(self):
        """Redraw scene."""
        self.clear()
        self.gui.draw_label(self.score)
        self.draw_cell(self.game.food_pos, Color.RED)
        for cell in self.game.snake.cells:
            self.draw_cell(cell, Color.GRAY)
        self.draw_cell(self.game.snake.head, Color.WHITE)

    def reset(self):
        """Drop game and start new one."""
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score.text = "0"
        self.game.score = 0

# TODO Move colors into config
# TODO Replace draw_label with label.redraw
# TODO Make label regular child
