"""" This package defines various Event related functionality. """

from .event import Event
from .keyevent import KeyEvent, KEY_PRESSED, KEY_RELEASED
from .mouseevent import MouseButtonEvent, MouseMotionEvent
from .exitevent import ExitEvent

__all__ = ("Event", "KeyEvent", "MouseButtonEvent", "MouseMotionEvent", "ExitEvent")
