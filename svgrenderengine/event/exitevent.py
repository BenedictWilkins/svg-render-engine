""" Module defining the ExitEvent class. ExitEvent is used to signal that the program should close."""

from dataclasses import dataclass
from .event import Event  # Assuming Event class is defined in the 'event' module


@dataclass
class ExitEvent(Event):

    """A class representing a program exit event.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
    """
