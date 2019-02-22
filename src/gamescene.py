"""Module contains scene for playing Snak."""

from MWidgets import Scene, Widget, Event, Color, ColorRole
from game import Game


class GameScene(Scene):
    """Visual representation of game."""

    def __init__(self, rect, parent, cell_size, fps):
        """Create new scene with, cell size and parent."""
        super().__init__(rect, parent)
        *_, w, h = self.rect
        self.cell_size = cell_size

        self.game = Game(w//self.cell_size, h//self.cell_size)

        self.speed = 40//fps
        if self.speed == 0:
            raise "Max fps value is 40"
        self.update_count = 0
        self.stored_events = list()

        self.events = {
            **self.events,
            "Paused": Event.Type.Custom0,
            "Closed": Event.Type.Custom1,
            "New_score": Event.Type.Custom2
        }
        self.triggers = {
            **self.triggers,
            "reset": self.reset,
            "pause_game": self.pause_game,
            "move_left": self.move_left,
            "move_right": self.move_right,
            "move_up": self.move_up,
            "move_down": self.move_down
        }

    @classmethod
    def from_config(cls, config, parent):
        """Load scene from config."""
        ret = cls(config["rect"],
                  parent,
                  config["cell_size"],
                  config["fps"])
        return ret

    def add_child(self, id, child):
        """Override parents add_child to set score label."""
        super().add_child(id, child)
        if id == "score_label":
            palette = child.palette[Widget.State.Active]
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
        self.stored_events += events
        self.update_count = (self.update_count + 1) % self.speed
        if self.update_count != 0:
            return

        super().update(self.stored_events)
        self.stored_events.clear()

        score = self.game.score
        self.game.make_move()
        if self.game.score != score:
            self.emmit_event(Event.Type.Custom2, str(self.game.score))
        if self.game.snake.is_selfcrossed():
            self.emmit_event(Event.Type.Custom1)

    def redraw(self):
        """Redraw scene."""
        super().redraw()

        w, h = self.cell_size, self.cell_size
        x, y = self.game.food_pos
        self.draw_rect((x*self.cell_size, y*self.cell_size, w, h),
                       Color.RED)

        for cell in self.game.snake.cells:
            x, y = cell
            self.draw_rect((x*self.cell_size, y*self.cell_size, w, h),
                           Color.GRAY)

        x, y = self.game.snake.head
        self.draw_rect((x*self.cell_size, y*self.cell_size, w, h),
                       Color.WHITE)

    def reset(self):
        """Drop game and start new one."""
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.game.score = 0
        self.emmit_event(Event.Type.Custom2, "0")

# TODO Move colors into config
