import time
from gui import GUI
from gamescene import GameScene
from mwidgets import Window, Loader, Widget
from mwidgets import Event


class MainWindow(Window):
    def __init__(self, config, _):
        Loader.register_widget("GameScene", GameScene)
        *_, w, h = config["rect"]
        gui = GUI(w, h)
        super().__init__(config, gui=gui)
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
        events = list()
        while playing:
            events += self.gui.check_events()
            for event in events:
                if not event.source:
                    event.source = self
                if event.type == Event.Type.Quit:
                    playing = False
            events = self.update(events)
            self.gui.update()
            time.sleep(1.0/self.fps)

    def update(self, events):
        ret = self.process_events(events)
        ret += self.layout.update(events)
        return ret

    def pause_game(self):
        self.fps = 20
        self.layout = self.children["pause_menu"]
        return []

    def continue_game(self):
        self.layout = self.children["game_scene"]
        self.fps = 8
        return []

    def open_main_menu(self):
        self.fps = 20
        self.layout = self.children["main_menu"]
        return []

    def open_evolution_menu(self):
        self.fps = 20
        self.layout = self.children["evolution_menu"]
        return []

    def start_new_game(self):
        self.layout = self.children["game_scene"]
        self.layout.reset()
        self.fps = 8
        return []
