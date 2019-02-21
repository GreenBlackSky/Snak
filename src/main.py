"""Executive module of game."""

import sys
from MWidgets import Loader
from mainwindow import MainWindow
from gamescene import GameScene


if __name__ == "__main__":
    Loader.register_widget("MainWindow", MainWindow)
    Loader.register_widget("GameScene", GameScene)
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    main_window = Loader.load_yaml(path)
    main_window.exec()
