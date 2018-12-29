from widgets import Widget, Scene, Label
from events import Event
from game import Game
from colors import Color, ColorRole

class GameScene(Scene):
    KEYS = {Event.Key.K_UP: (0, -1),
            Event.Key.K_DOWN: (0, 1),
            Event.Key.K_LEFT: (-1, 0),
            Event.Key.K_RIGHT: (1, 0)}

    def __init__(self, parent, gui, config):
        super().__init__(parent, gui, config)
        self.cell_size = config["cell_size"]
        *_, w, h = self.rect
        self.game = Game(w//self.cell_size, h//self.cell_size)
        self.parent = parent
        self.score = Label((w*0.4, 0, h*0.2, h*0.2), gui, '0')
        self.score.palette[Widget.State.Active][ColorRole.Foreground] = Color.BLACK
        self.score.palette[Widget.State.Active][ColorRole.Text] = Color.DARK_GRAY
        self.redraw()

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