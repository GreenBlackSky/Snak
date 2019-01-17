from mwidgets import Scene, Label, Widget, Event, Color, ColorRole
from game import Game


class GameScene(Scene):
    KEYS = {Event.Key.K_UP: (0, -1),
            Event.Key.K_DOWN: (0, 1),
            Event.Key.K_LEFT: (-1, 0),
            Event.Key.K_RIGHT: (1, 0)}

    def __init__(self, config, parent):
        super().__init__(config, parent)
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score = Label(config["Label"], self)
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY

    def update(self, events):
        for event in events:
            if event.type == Event.Type.KeyPressed:
                if event.data == Event.Key.K_ESCAPE:
                    self.parent.pause_game()
                    break
                if event.data in GameScene.KEYS:
                    self.game.snake_mind.desire(GameScene.KEYS[event.data])
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            self.parent.open_main_menu()
        self.redraw()
        return super().update(events)

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

# TODO Move event-logic into config
# TODO create events instead of calling parent methods
