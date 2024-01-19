from dataclasses import dataclass
from ..event import Event
from typing import Dict, List, Any


@dataclass
class ResponseEvent(Event):
    """Class for representing a response to a QueryEvent in SVG file manipulations.

    This class composes an Event to track the basic event information and extends it
    with additional details specific to the response of a QueryEvent.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
        query_event_id (str): The ID of the QueryEvent that triggered this response.
        success (bool): Indicates whether the associated QueryEvent was successful.
        data (dict): Holds relevant data for the response. For SELECT queries,
                     this contains the selected attribute values.
    """

    query_event_id: str
    success: bool
    data: Dict[str, Any] = None

    @staticmethod
    def new(query_event_id: str, success: str, data: Dict[str, Any]):
        """Creates a new instance of `ResponseEvent` as a tuple with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `query_event_id`, `success` and `data` fields.

            This method generates a UUID4, converts it to a string, and gets the current UNIX time (in seconds) to be used as the event's `id` and `timestamp` respectively.
        Returns:
            Event: A new tuple instance with a unique `id`, a `timestamp` and the provided `query_event_id`, `success` and `data`  fields.
        """
        return (*Event.new(), query_event_id, success, data)

    @staticmethod
    def create_event(query_event_id: str, success: str, data: Dict[str, Any]):
        """Creates a new instance of `ResponseEvent` with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `query_event_id`, `success` and `data` fields.

            See also: `ResponseEvent.new`

        Returns:
            Event: A new instance of the ResponseEvent class with a unique ID and a timestamp.
        """
        return ResponseEvent(*ResponseEvent.new(query_event_id, success, data))
