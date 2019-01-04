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

    def set_callbacks(self):
        self.children["main_menu"].children["new_game_button"].callbacks[Widget.Slots.Clicked].append(self.start_new_game)
        self.children["main_menu"].children["open_evolution_menu_button"].callbacks[Widget.Slots.Clicked].append(self.open_evolution_menu)
        self.children["pause_menu"].children["continue_game_button"].callbacks[Widget.Slots.Clicked].append(self.continue_game)
        self.children["pause_menu"].children["start_new_game_button"].callbacks[Widget.Slots.Clicked].append(self.start_new_game)
        self.children["pause_menu"].children["main_menu_from_pause_button"].callbacks[Widget.Slots.Clicked].append(self.open_main_menu)
        self.children["evolution_menu"].children["main_menu_from_evolution_button"].callbacks[Widget.Slots.Clicked].append(self.open_main_menu)
    
    def play(self):
        playing = True
        while playing:
            events = self.gui.check_events()
            for event in events:
                if event.type == Event.Type.Quit:
                    playing = False
        
            self.layout.update(events)
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

# TODO callbacks from config
