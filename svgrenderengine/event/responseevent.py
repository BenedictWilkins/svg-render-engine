from dataclasses import dataclass
from ..event import Event


@dataclass
class ResponseEvent:
    """Class for representing a response to a QueryEvent in SVG file manipulations.

    This class composes an Event to track the basic event information and extends it
    with additional details specific to the response of a QueryEvent.

    Attributes:
        event (Event): The general event associated with this response event.
        query_event_id (str): The ID of the QueryEvent that triggered this response.
        success (bool): Indicates whether the associated QueryEvent was successful.
        data (dict): Holds relevant data for the response. For select queries,
                     this contains the selected attribute values.
    """

    event: Event
    query_event_id: str
    success: bool
    data: dict = None
