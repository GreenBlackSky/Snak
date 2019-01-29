import sys
import yaml
from mainwindow import MainWindow
from mwidgets import Loader
from gui import GUI


if __name__ == "__main__":
    # Load config
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    file = open(path, 'r')
    config = yaml.safe_load(file)
    file.close()
    # Initialize gui
    *_, w, h = config["rect"]
    gui=GUI(w, h)
    # Load application
    Loader.register_widget("MainWindow", MainWindow)
    main_window = Loader.load(config)
    main_window.set_gui(gui)
    # Start exec loop
    main_window.exec()

# TODO Document basic widgets and thier roles
