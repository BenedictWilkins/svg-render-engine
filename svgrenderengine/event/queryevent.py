""" Module defining the QueryEvent class. Query is used to update, select or delete SVG elements and their attributes. """

from dataclasses import dataclass
from .event import Event


@dataclass
class QueryEvent:
    """Class for representing an event that manipulates SVG files.

    This class extends the Event class to include functionality for SVG file manipulation,
    such as updating, selecting, or deleting elements and their attributes.

    Attributes:
        event (Event): The general event associated with this query event.
        action (str): The type of action to be performed (e.g., 'update', 'select', 'delete').
        element_id (str): The ID of the SVG element to be manipulated.
        attributes (dict): The attributes to be updated or used for selection.
                           For deletion, this can be empty.
     Static Fields:
        UPDATE (str): Represents an update action.
        SELECT (str): Represents a select action.
        DELETE (str): Represents a delete action.
    """

    UPDATE = "update"
    SELECT = "select"
    DELETE = "delete"

    event: Event
    action: str
    element_id: str
    attributes: dict | list
