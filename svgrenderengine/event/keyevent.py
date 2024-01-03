""" Module defining the KeyEvent class. KeyEvent is used to represent user keyboard input."""

from dataclasses import dataclass
from .event import Event  # Assuming Event class is defined in the 'event' module

KEY_PRESSED = "pressed"
KEY_RELEASED = "released"


@dataclass
class KeyEvent:

    """A class representing a keyboard event, composed of a general event.

    Attributes:
        event (Event): The event associated with this keyboard event.
        key (int): The key code of the keyboard event.
        key_name (str): The name of the key pressed or released.
        status (str): The status of the key event ('pressed', 'released').
    """

    event: Event
    key: int
    key_name: str
    status: str
