""" Module defining the ExitEvent class. ExitEvent is used to signal that the program should close."""

from dataclasses import dataclass
from .event import Event  # Assuming Event class is defined in the 'event' module


@dataclass
class ExitEvent:

    """A class representing a program exit event, composed of a general event.

    Attributes:
        event (Event): The event associated with this keyboard event.
    """

    event: Event
