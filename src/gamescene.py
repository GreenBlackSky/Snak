from mwidgets import Scene, Label, Widget, Event, Color, ColorRole
from game import Game


class GameScene(Scene):
    def __init__(self, config, parent):
        super().__init__(config, parent)
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.fps = config["fps"]
        self.score = Label(config["Label"], self)
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY
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
            "move_down": self.move_down
        }

    def pause_game(self):
        self.event_queue.append(Event(Event.Type.Custom0, self))

    def move_left(self):
        self.game.snake_mind.desire((-1, 0))

    def move_right(self):
        self.game.snake_mind.desire((1, 0))

    def move_up(self):
        self.game.snake_mind.desire((0, -1))

    def move_down(self):
        self.game.snake_mind.desire((0, 1))

    def update(self, events):
        super().update(events)
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            self.event_queue.append(Event(Event.Type.Custom1, self))
        self.redraw()

    def redraw(self):
        self.clear()
        self.gui.draw_label(self.score)
        self.draw_cell(self.game.food_pos, Color.RED.value)
        for cell in self.game.snake.cells:
            self.draw_cell(cell, Color.GRAY.value)
        self.draw_cell(self.game.snake.head, Color.WHITE.value)

    def reset(self):
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score.text = "0"
        self.game.score = 0

# TODO Move colors into config
# TODO Move label into config