""" Module defining the KeyEvent class. KeyEvent is used to represent user keyboard input."""

from dataclasses import dataclass
from .event import Event  # Assuming Event class is defined in the 'event' module

KEY_PRESSED = "pressed"
KEY_RELEASED = "released"


@dataclass
class KeyEvent(Event):

    """A class representing a keyboard event.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
        key (int): The key code of the keyboard event.
        key_name (str): The name of the key pressed or released.
        status (str): The status of the key event ('pressed', 'released').
    """

    key: int
    key_name: str
    status: str
