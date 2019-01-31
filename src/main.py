import sys
import yaml
from mwidgets import Loader
from mainwindow import MainWindow
from gamescene import GameScene
from gui import GUI


if __name__ == "__main__":
    # Load config
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    file = open(path, 'r')
    config = yaml.safe_load(file)
    file.close()
    # Initialize gui
    *_, w, h = config["rect"]
    gui = GUI(w, h)
    # Load application
    loader = Loader()
    loader.register_widget("MainWindow", MainWindow)
    loader.register_widget("GameScene", GameScene)
    main_window = loader.load(config)
    loader.clean()
    main_window.set_gui(gui)
    # Start exec loop
    main_window.exec()

# TODO Document basic widgets and thier roles
