from enum import Enum
from colors import Color, ColorRole
from events import Event


class Signal(Enum):
    StartNewGame = 0,
    PauseGame = 1,
    OpenEvolutionMenu = 2,
    ContinueGame = 3,
    OpenMainMenu = 4,
    YouLoose = 5,
    NewHighScore = 6


class Widget:
    class State(Enum):
        Active = 0
        Inactive = 1
        Highlighted = 2
        Pressed = 3

    @staticmethod
    def default_palette():
        return {
            Widget.State.Active: {
                ColorRole.Background: Color.BLACK,
                ColorRole.Foreground: Color.GRAY,
                ColorRole.Text: Color.WHITE
            },
            Widget.State.Inactive: {
                ColorRole.Background: Color.BLACK,
                ColorRole.Foreground: Color.DARK_GRAY,
                ColorRole.Text: Color.BLACK
            },
            Widget.State.Highlighted: {
                ColorRole.Background: Color.BLACK,
                ColorRole.Foreground: Color.WHITE,
                ColorRole.Text: Color.GRAY
            },
            Widget.State.Pressed: {
                ColorRole.Background: Color.BLACK,
                ColorRole.Foreground: Color.RED,
                ColorRole.Text: Color.BLACK
            }
        }

    def __init__(self, rect):
        self.rect = rect
        self.focusable = False
        self.state = Widget.State.Active
        self.palette = Widget.default_palette()

    def inside(self, cx, cy):
        x, y, w, h = self.rect
        return x < cx < x + w and y < cy < y + h

    def is_focusable(self):
        return self.focusable and self.state == Widget.State.Active

    def set_active(self, val):
        if val and self.state == Widget.State.Inactive:
            self.state = Widget.State.Active
        elif not val:
            self.state = Widget.State.Inactive

    def is_active(self):
        return self.state != Widget.State.Inactive


class Button(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text
        self.focusable = True

    def highlight(self):
        if self.state == Widget.State.Active:
            self.state = Widget.State.Highlighted

    def diminish(self):
        if self.state == Widget.State.Highlighted:
            self.state = Widget.State.Active

    def press(self):
        if self.state == Widget.State.Highlighted:
            self.state = Widget.State.Pressed

    def is_pressed(self):
        return self.state == Widget.State.Pressed

    def release(self):
        if self.state == Widget.State.Pressed:
            self.state = Widget.State.Highlighted

    def update(self, events):
        if not self.is_active():
            return
        mouse_pressed = False
        mouse_released = False
        return_pressed = False
        return_released = False
        mx, my = None, None
        for event in events:
            if event.type == Event.Type.MousePressed:
                mouse_pressed = True
            elif event.type == Event.Type.MouseReleased:
                mouse_released = True
            elif event.type == Event.Type.MouseState:
                mx, my, _ = event.data
            elif event.type == Event.Type.KeyPressed and event.data == Event.Key.K_RETURN:
                return_pressed = True
            elif event.type == Event.Type.KeyReleased and event.data == Event.Key.K_RETURN:
                return_released = True
        ret = False
        if return_pressed or (self.inside(mx, my) and mouse_pressed):
            self.press()
        if self.state == Widget.State.Pressed and (mouse_released or return_released):
            self.release()
            if self.inside(mx, my) or return_released:
                ret = True
        return ret


class TextList(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class TextInput(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class Label(Widget):
    def __init__(self, rect, text):
        super().__init__(rect)
        self.text = text


class CheckBox(Widget):
    def __init__(self, rect):
        super().__init__(rect)


class Window(Widget):
    def __init__(self, rect, redraw):
        super().__init__(rect)
        self.redraw = redraw
        self.focus = None
        self.widgets = []
        self.focus_order = []
        self.callbacks = {}


class Menu(Window):
    def __init__(self, rect, redraw, config):
        super().__init__(rect, redraw)
        x, y, w, h = self.rect
        for widget_cfg in config:
            # Create widget
            xm, ym, wm, hm = widget_cfg["rect"]
            rect = (x + w*xm, y + h*ym, w*wm, h*hm)
            widget = eval(widget_cfg["type"])(rect, widget_cfg["capture"])
            # Activate widget
            if not widget_cfg.get("active", True):
                widget.set_active(False)
            # Add widget to focus_order and widgets
            self.widgets.append(widget)
            if widget.is_focusable():
                self.focus_order.append(widget)
            # set callback
            if "callback" not in widget_cfg:
                self.callbacks[widget] = None
            else:
                self.callbacks[widget] = Signal[widget_cfg["callback"]]
        if not self.focus_order:
            raise "No focusable on form"
        self.focus = self.focus_order[0]
        self.focus.highlight()
        self.redraw(self)

    def update(self, events):
        # Process events
        focus_n = self.focus_order.index(self.focus)
        mx, my = None, None
        for event in events:
            if event.type == Event.Type.KeyPressed:
                if event.data == Event.Key.K_UP:
                    focus_n -= 1
                elif event.data == Event.Key.K_DOWN:
                    focus_n += 1
            elif event.type == Event.Type.MouseState:
                mx, my, _ = event.data
        focus_n = max(focus_n, 0)
        focus_n = min(focus_n, len(self.focus_order) - 1)
        # Check focus
        ret = None
        if self.focus.update(events):
            ret = self.callbacks[self.focus]
        # Move focus
        if not self.focus.is_pressed():
            old_focus = self.focus
            for widget in self.focus_order:
                widget.diminish()
                if widget.inside(mx, my):
                    self.focus = widget
            if old_focus == self.focus:
                self.focus = self.focus_order[focus_n]
        # Redraw
        self.focus.highlight()
        self.redraw(self)
        return ret


class Scene(Window):
    def __init__(self, rect, redraw):
        super().__init__(rect, redraw)

# TODO events
# TODO load
# TODO redraw