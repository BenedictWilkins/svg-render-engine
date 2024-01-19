""" Module defining the MouseButtonEvent and MouseMotionEvent classes. """

from typing import List
from dataclasses import dataclass
from .event import Event  # Assuming Event is defined in the 'event' module

__all__ = ("MouseButtonEvent", "MouseMotionEvent")


@dataclass
class MouseButtonEvent(Event):
    """
    A class representing a mouse event.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
        button (int): The mouse button involved in the event (1 for left click, 2 for middle click, 3 for right click, etc.).
        position (tuple): The (x, y) coordinates of the mouse event.
        status (str): The status of the mouse event ('pressed', 'released').
    """

    button: int
    position: tuple
    status: str
    # element: List[str] # element (List[str]): A list of svg elements ('id' tag) that are under the mouse pointer.


@dataclass
class MouseMotionEvent(Event):
    """
    A class representing a mouse moition event.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).        position (tuple): The (x, y) coordinates of the mouse event.
        relative (tuple): The relative motion of the mouse since the last event.
    """

    position: tuple
    relative: tuple
