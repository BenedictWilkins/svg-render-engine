""" Module defining the Event class."""
import uuid
from dataclasses import dataclass
import time


@dataclass
class Event:
    """A simple Event class with a unique identifier and a timestamp.

    Attributes:
        id (str): A unique identifier for the event, represented as a string.
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created.
    """

    id: str
    timestamp: float

    @staticmethod
    def new():
        """Creates a new instance of Event as a tuple with a unique UUID as its id and a current UNIX timestamp.

        The intended use is when instantiating subclasses of event. For example, MouseButtonEvent(*Event.new(), ...)

        Returns:
            Event: A new tuple instance with a unique ID and a timestamp.
        """
        return (str(uuid.uuid4()), time.time())

    @staticmethod
    def create_event():
        """Creates a new instance of Event with a unique UUID as its id and a current UNIX timestamp.

        This method generates a UUID4, converts it to a string, and gets the current UNIX time (in seconds) to be used as the event's ID and timestamp respectively.

        Returns:
            Event: A new instance of the Event class with a unique ID and a timestamp.
        """
        return Event(id=str(uuid.uuid4()), timestamp=time.time())
