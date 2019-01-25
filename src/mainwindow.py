import time
from gui import GUI
from gamescene import GameScene
from mwidgets import Window, Loader, Widget
from mwidgets import Event


class MainWindow(Window):
    def __init__(self, config, _):
        Loader.register_widget("GameScene", GameScene)
        *_, w, h = config["rect"]
        super().__init__(config, gui=GUI(w, h))
        self.highscore = 0
        self.triggers = {
            **self.triggers,
            "pause_game": self.pause_game,
            "continue_game": self.continue_game,
            "open_main_menu": self.open_main_menu,
            "open_evolution_menu": self.open_evolution_menu,
            "start_new_game": self.start_new_game
        }

    def play(self):
        playing = True
        while playing:
            events = list(self.event_queue)
            events += self.gui.check_events()
            self.event_queue.clear()
            for event in events:
                if not event.source:
                    event.source = self
                if event.type == Event.Type.Quit:
                    playing = False
            self.update(events)
            self.gui.update()
            time.sleep(1.0/self.fps)

    def pause_game(self):
        self.fps = 20
        self.layout = self.children["pause_menu"]

    def continue_game(self):
        self.layout = self.children["game_scene"]
        self.fps = 8

    def open_main_menu(self):
        self.fps = 20
        self.layout = self.children["main_menu"]

    def open_evolution_menu(self):
        self.fps = 20
        self.layout = self.children["evolution_menu"]

    def start_new_game(self):
        self.layout = self.children["game_scene"]
        self.layout.reset()
        self.fps = 8

# TODO Make fps constant
