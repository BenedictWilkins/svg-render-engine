""" 
    Module defining the QueryEvent and QuerySVGEvent classes. 

    A QuerySVGEvent is used to update, select, delete or insert SVG elements or attributes. 
    A QueryEvent is used to update or select templated state variables that are part of the SVG code. 
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from .event import Event


@dataclass
class QueryEvent(Event):
    """
    Represents a query event used to interact with a data structure.

    This class is intended for use in operations such as updating or selecting (accessing) attributes. It supports dot notation for accessing nested values.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
        action (int): Specifies the type of query event. This can be 'UPDATE' for updating values in a data structure, or 'SELECT' for retrieving values. `action` is a flag may be `Application` dependant, see associated documentation for details. See below for details on each action flag.
        attributes (dict | list): Defines the attributes to be updated or selected in the data structure. For 'update' operations, this should be a dictionary of {path: new_value}. For 'select' operations, this should be a list of paths.

    Action flags:
        SELECT = 0              # SELECT action to get a value using the keys specfied in `attributes`.
        UPDATE = 1              # UPDATE action to change a value using the keys specfied in `attributes`.
        SELECT_TEMPLATE = 2     # TODO
        UPDATE_TEMPLATE = 3     # TODO
        SELECT_RENDERED = 4     # TODO
    """

    action: int
    attributes: Dict[str, Any] | List[str]

    # static constant (actions)
    SELECT = 0
    UPDATE = 1
    SELECT_TEMPLATE = 2
    UPDATE_TEMPLATE = 3
    SELECT_RENDERED = 4

    @staticmethod
    def new(action: int, attributes: List[str] | Dict[str, str]):
        """Creates a new instance of `QueryEvent` as a tuple with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `action`, and `attributes` fields.

            This method generates a UUID4, converts it to a string, and gets the current UNIX time (in seconds) to be used as the event's `id` and `timestamp` respectively.
        Returns:
            Event: A new tuple instance with a unique `id`, a `timestamp` and the provided `action`, and `attributes` fields.
        """
        assert isinstance(attributes, (list, dict))
        return (*Event.new(), action, attributes)

    @staticmethod
    def create_event(action: int, attributes: List[str] | Dict[str, str]):
        """Creates a new instance of `QueryEvent` with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `action`, and `attributes` fields.

            See also: `QueryEvent.new`

        Returns:
            Event: A new instance of the Event class with a unique ID and a timestamp.
        """
        return QueryEvent(*QueryEvent.new(action, attributes))


@dataclass
class QuerySVGEvent(QueryEvent):
    """Class for representing an event that manipulates SVG (or XML) data.

    This class extends the `Event` class to include functionality for SVG file manipulation,
    such as updating, selecting, deleting or inserting elements and their attributes.

    Attributes:
        id (str): A unique identifier for the event, represented as a string (inherited).
        timestamp (float): The UNIX timestamp (in seconds) when the event instance is created (inherited).
        action (str): The type of action to be performed (e.g., 'update', 'select', 'delete').
        element_id (str): The ID of the SVG element to be manipulated.
        attributes (dict): The attributes to be updated or used for selection.
                           For deletion, this can be empty.
    """

    element_id: str

    @staticmethod
    def from_query_event(
        query_event: QueryEvent, variable_open: str = r"{{", variable_close: str = r"}}"
    ) -> List["QuerySVGEvent"]:
        """
        Converts a `QueryEvent` into a list of `QuerySVGEvents`, grouping by `element_id`, which is taken to be the first part of the dot-seperated keys in the `query_event` attributes.

        Args:
            query_event (QueryEvent): The `QueryEvent` to convert.
            variable_open (str) : value used to indicate the start of a variable block to make it XML compatible, this will replace `{{` in the query.
            variable_close (str) : value used to indicate the end of a variable block to make it XML compatible, this will replace `}}` in the query.
        Returns:
            List[QuerySVGEvent]: A list of `QuerySVGEvent` instances.
        """
        event_list = []
        element_attrs = {}

        if isinstance(query_event.attributes, dict):
            # Grouping attributes by their element_id
            for key in query_event.attributes:
                try:
                    element_id, attr_key = split_by_first_dot(
                        key, variable_open, variable_close
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Failed to cast {QueryEvent.__name__} to {QuerySVGEvent.__name__}, attribute {key} is not dot-seperated.",
                    ) from e

                if element_id not in element_attrs:
                    element_attrs[element_id] = {}
                element_attrs[element_id][attr_key] = query_event.attributes[key]

        elif isinstance(query_event.attributes, list):
            # Grouping attributes by their element_id
            for key in query_event.attributes:
                # try:
                element_id, *attr_key = split_by_first_dot(
                    key, variable_open, variable_close
                )

                # except ValueError as e:
                #     raise ValueError(
                #         f"Failed to cast {QueryEvent.__name__} to {QuerySVGEvent.__name__}, attribute {key} is not dot-seperated.",
                #     ) from e

                if element_id not in element_attrs:
                    element_attrs[element_id] = []
                if len(attr_key) == 1:
                    # this means there was an attribute, otherwise leave element_attrs[element_id] empty (this means select all)
                    element_attrs[element_id].append(attr_key[0])
        else:
            # TODO extract this error string / make custom error
            raise ValueError(
                f"Invalid type for {QueryEvent.__name__} attributes: {type(query_event.attributes)}, must be list or dict."
            )

        # Creating QuerySVGEvents for each element_id
        for element_id, attrs in element_attrs.items():
            svg_event = QuerySVGEvent.create_event(
                query_event.action, element_id, attrs
            )
            event_list.append(svg_event)

        return event_list

    @staticmethod
    def new(action, element_id: str, attributes: List[str] | Dict[str, str] = None):
        """Creates a new instance of `QuerySVGEvent` as a tuple with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `action`, `element_id` and `attributes` fields.

            This method generates a UUID4, converts it to a string, and gets the current UNIX time (in seconds) to be used as the event's `id` and `timestamp` respectively.
            Note that if `attributes` is a `dict`, its values will be will be converted to `str` using `str(...)`.
        Returns:
            Event: A new tuple instance with a unique `id`, a `timestamp` and the provided `action`, `element_id` and `attributes` fields.
        """
        if attributes is None:
            if action == QuerySVGEvent.UPDATE:
                attributes = dict()
            elif action == QuerySVGEvent.SELECT:
                attributes = list()
        if isinstance(attributes, dict):
            attributes = {k: str(v) for k, v in attributes.items()}
            if len(attributes) == 0:
                raise ValueError(
                    f"Action {QuerySVGEvent.UPDATE} requires at least one attribute to update."
                )
        return (*Event.new(), action, element_id, attributes)

    @staticmethod
    def create_event(action, element_id, attributes=None):
        """Creates a new instance of `QuerySVGEvent` with a unique UUID as its `id`, a current UNIX `timestamp`, the provided `action`, `element_id` and `attributes` fields.

            See also: `QuerySVGEvent.new`

        Returns:
            Event: A new instance of the Event class with a unique ID and a timestamp.
        """
        return QuerySVGEvent(*QuerySVGEvent.new(action, attributes, element_id))


def split_by_first_dot(
    value: str, variable_open: str = r"{{", variable_close: str = r"}}"
):
    """Splits a key by the first occurrence of a dot, while handling variable templating properly.

    Args:
        value (str): string to split by first dot.
        variable_open (str): value used to indicate the start of a variable block.
        variable_close (str): value used to indicate the end of a variable block.

    Returns:
        Tuple[str, str]: the split string. A tuple-1 if no dot is present (outside a template block).
    """

    first, *rest = value.split(".", 1)
    # print(value, variable_open, variable_close)
    if not variable_open in first:
        return first, *rest
    else:
        # there is potentially a template to deal with.
        inside_variable_block = 0
        open_len = len(variable_open)
        close_len = len(variable_close)
        i = 0
        while i < len(value):
            if value[i : i + open_len] == variable_open:
                inside_variable_block += 1
                i += open_len
            elif value[i : i + close_len] == variable_close:
                inside_variable_block = max(0, inside_variable_block - 1)
                i += close_len
            elif value[i] == "." and inside_variable_block == 0:
                return value[:i], value[i + 1 :]
            else:
                i += 1
        return (value,)


# def split_by_first_dot(
#     value: str, variable_open: str = r"{{", variable_close: str = r"}}"
# ):
#     """Splits a key by the first occurance of a dot, while handling variable templating properly.

#     Args:
#         value (str): string to split by first dot.
#         variable_open (str) : value used to indicate the start of a variable block.
#         variable_close (str) : value used to indicate the end of a variable block.

#     Returns:
#         (Tuple(first, rest)): the split string. A tuple-1 if no dot is present (outside a template block).
#     """
#     first, *rest = value.split(".", 1)
#     if not variable_open in first:
#         return first, *rest
#     else:
#         # there may be dots inside a template expression, these need to be handled correctly.
#         inside_braces = 0
#         for i, char in enumerate(value):
#             if char == "{":
#                 inside_braces += 1
#             elif char == "}":
#                 inside_braces = max(0, inside_braces - 1)
#             elif char == "." and inside_braces == 0:
#                 return value[:i], value[i + 1 :]
#         return (value,)
