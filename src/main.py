import pygame
import time
import sys
import yaml
from gui import *
from widgets import *


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cfg/menu.yaml"
    stream = open(path, 'r')
    cfg  = yaml.load(stream)
    main_window = Widget.load(cfg)
    x, y, w, h = main_window.rect
    gui = GUI(w, h)

    que = [main_window]
    while que:
        widget = que.pop()
        widget.set_painter(gui)
        que += widget.get_children()

    events = list()
    while True:
        events += gui.get_events()
        events = main_window.update(events)
        if Widget.Signal.Exit in events:
            break
        gui.update()
        time.sleep(0.05)


