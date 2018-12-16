import pygame
from widgets import *
from gui import GUI

    
if __name__ == "__main__":
    gui = GUI(80, 40, 10)
    while True:
        events = gui.check_events()
        signal = gui.form.update(events)
        if signal is not None:
            gui.update(signal)
        pygame.display.update()
        time.sleep(1.0/gui.fps)
