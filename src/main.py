"""Executive module of game."""

import sys

from mwidgets import Loader

from gamescene import GameScene
from mainwindow import MainWindow


if __name__ == "__main__":
    loader = Loader()
    loader.register_widget("GameScene", GameScene)
    loader.register_widget("MainWindow", MainWindow)
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    main_window = loader.load_yaml(path)
    main_window.exec()
