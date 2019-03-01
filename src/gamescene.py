"""Module contains scene for playing Snak."""

from mwidgets import Scene, Widget, Event, ValueEvent, Color, ColorRole
from game import Game


class CloseGameEvent(Event):
    """Create this event to finish game."""

    pass


class UpdateScoreEvent(ValueEvent):
    """Create this event when score is updated."""

    pass


class GameScene(Scene):
    """Visual representation of game."""

    def __init__(self, rect, parent, fps):
        """Create new scene with, cell size and parent."""
        super().__init__(rect, parent)
        *_, w, h = self.rect
        self.cell_side = 10

        self.game = Game(w//self.cell_side, h//self.cell_side)

        self.speed = 40//fps
        if self.speed == 0:
            raise "Max fps value is 40"
        self.update_count = 0
        self.stored_events = list()

        self.events = {
            **self.events,
            "Closed": CloseGameEvent,
            "New_score": UpdateScoreEvent
        }
        self.triggers = {
            **self.triggers,
            "reset": self.reset,
            "move_left": lambda: self.game.snake_mind.desire((-1, 0)),
            "move_right": lambda: self.game.snake_mind.desire((1, 0)),
            "move_up": lambda: self.game.snake_mind.desire((0, -1)),
            "move_down": lambda: self.game.snake_mind.desire((0, 1)),
            "big_field": lambda: self.set_cell_side(5),
            "average_field": lambda: self.set_cell_side(10),
            "small_field": lambda: self.set_cell_side(20)
        }

    @classmethod
    def from_config(cls, config, parent):
        """Load scene from config."""
        ret = cls(config.get("rect", [0, 0, 1, 1]),
                  parent,
                  config["fps"])
        return ret

    def add_widget(self, child, id):
        """Override parents add_widget to set score label."""
        super().add_widget(child, id)
        if id == "score_label":
            palette = child.palette[Widget.State.Active]
            palette[ColorRole.Foreground] = Color.BLACK
            palette[ColorRole.Text] = Color.DARK_GRAY

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
            self.emmit_event(UpdateScoreEvent, [str(self.game.score)])
        if self.game.snake.is_selfcrossed():
            self.emmit_event(CloseGameEvent)

    def redraw(self):
        """Redraw scene."""
        super().redraw()

        w, h = self.cell_side, self.cell_side
        x, y = self.game.food_pos
        self.draw_rect((x*self.cell_side, y*self.cell_side, w, h),
                       Color.RED)

        for cell in self.game.snake.cells:
            x, y = cell
            self.draw_rect((x*self.cell_side, y*self.cell_side, w, h),
                           Color.GRAY)

        x, y = self.game.snake.head
        self.draw_rect((x*self.cell_side, y*self.cell_side, w, h),
                       Color.WHITE)

    def reset(self):
        """Drop game and start new one."""
        *_, w, h = self.rect
        self.game = Game(w//self.cell_side, h//self.cell_side)
        self.game.score = 0
        self.emmit_event(UpdateScoreEvent, ["0"])

    def set_cell_side(self, size):
        """Chenge side of cell of a field."""
        self.cell_side = size

# TODO Move colors into config
# TODO Make snake and food and other objects children of scene
