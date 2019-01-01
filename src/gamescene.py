from mwidgets import Scene, Label, Widget, Event, Color, ColorRole
from game import Game


class GameScene(Scene):
    KEYS = {Event.Key.K_UP: (0, -1),
            Event.Key.K_DOWN: (0, 1),
            Event.Key.K_LEFT: (-1, 0),
            Event.Key.K_RIGHT: (1, 0)}

    def __init__(self, config, parent):
        super().__init__(config, parent)
        self.cell_size = config["cell_size"]
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.parent = parent
        self.score = Label(config["Label"], self)
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY

    def update(self, events):
        for event in events:
            if event.type == Event.Type.KeyPressed:
                if event.data == Event.Key.K_ESCAPE:
                    self.parent.pause_game()
                    return
                if event.data in GameScene.KEYS:
                    self.game.snake_mind.desire(GameScene.KEYS[event.data])
        self.game.make_move(self.game.get_next_move())
        self.score.text = str(self.game.score)
        if self.game.snake.is_selfcrossed():
            self.parent.open_main_menu()
            return
        self.redraw()

    def redraw(self):
        self.gui.draw_game(self)

    def reset(self):
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.score.text = "0"
        self.game.score = 0