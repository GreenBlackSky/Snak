import sys
import time
import yaml
from gui import GUI
from mainwindow import MainWindow
from mwidgets import Event


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    file = open(path, 'r')
    config = yaml.load(file)
    file.close()
    *_, w, h = config["rect"]
    cell_size = config["GameScene"]["cell_size"]
    gui = GUI(w//cell_size, h//cell_size, cell_size)
    main_window = MainWindow(gui, config)
    playing = True
    while playing:
        events = gui.check_events()
        for event in events:
            if event.type == Event.Type.Quit:
                playing = False
        
        main_window.layout.update(events)
        gui.update()
        time.sleep(1.0/main_window.fps)
