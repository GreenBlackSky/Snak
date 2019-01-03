import sys
import yaml
from mainwindow import MainWindow
from mwidgets import Loader


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    file = open(path, 'r')
    config = yaml.safe_load(file)
    file.close()
    Loader.register_widget("MainWindow", MainWindow)
    main_window = Loader.load_widget(config)
    main_window.set_callbacks()
    main_window.play()