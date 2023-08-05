import abc


class AsyncTickHandler(abc.ABC):
    @abc.abstractmethod
    def async_tick(self, window):
        """Update user input"""


class UserInputHandler(abc.ABC):
    @abc.abstractmethod
    def update_user_input(self, window):
        """Update user input"""


class KeyEventHandler(abc.ABC):
    @abc.abstractmethod
    def event_key(self, window, key, scancode, action, mods):
        """Keyboard event handler"""


class MouseButtonEventHandler(abc.ABC):
    @abc.abstractmethod
    def event_mouse_button(self, window, button, action, mods):
        """Mouse button event handler"""


class ScrollEventHandler(abc.ABC):
    @abc.abstractmethod
    def event_scroll(self, window, x_offset, y_offset):
        """Mouse scroll event handler"""


class CursorPosEventHandler(abc.ABC):
    @abc.abstractmethod
    def event_cursor_pos(self, window, x, y):
        """Mouse position event handler"""


class WindowSizeEventHandler(abc.ABC):
    @abc.abstractmethod
    def event_window_size(self, window, new_width, new_height):
        """Reshape window event handler"""
