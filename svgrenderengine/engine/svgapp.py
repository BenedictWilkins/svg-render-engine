import ast
from lxml import etree as ET
import html
from itertools import chain

from svgrenderengine.event.queryevent import QueryEvent

from ..event import QuerySVGEvent, ResponseEvent, Event


class SVGApplication:
    def __init__(self, file=None, svg_code=None):
        if file:
            with open(file, "r") as svg_file:
                svg_code = svg_file.read()
        elif svg_code:
            pass
        else:
            raise ValueError("Argument `file` or `svg_code` must be specified.")
        self.element_tree_root = ET.fromstring(svg_code)

    def query(self, query_event: QuerySVGEvent):
        assert isinstance(query_event, QuerySVGEvent)
        if query_event.action == QueryEvent.UPDATE:
            return SVGApplication.update(self.element_tree_root, query_event)
        # elif query_event.action == QueryRawEvent.DELETE:
        #    return SVGApplication.delete(self.element_tree_root, query_event)
        elif query_event.action == QueryEvent.SELECT:
            return SVGApplication.select(self.element_tree_root, query_event)

    @staticmethod
    def update(root: ET._Element, query_event: QuerySVGEvent) -> ResponseEvent:
        """Updates an SVG element based on the details provided in a QueryEvent instance,
        and returns a ResponseEvent indicating the outcome.

        Args:
            root (ET.Element): The root of the SVG element tree.
            query_event (QueryEvent): The query event containing update details.

        Returns:
            ResponseEvent: The response event indicating the outcome of the update operation.
        """
        # Initialize a ResponseEvent
        response = ResponseEvent.create_event(
            query_event_id=query_event.id,
            success=True,
            data=dict(),
        )

        # Check if the root itself is the element to be selected
        if root.get("id", None) == query_event.element_id:
            svg_element = root
        else:
            # Find the SVG element by ID among the children
            svg_elements = root.xpath(f".//*[@id='{query_event.element_id}']")
            svg_element = svg_elements[0] if svg_elements else None

        # Check if the element exists
        if svg_element is None:
            # TODO reason for failure in data? - element not found...
            response.success = False
            return response

        svg_element = svg_elements[0]

        # handle _inner_xml and _xml attributes...
        if "_inner_xml" in query_event.attributes:
            # TODO what happens if the element is not a container? test this
            replace_element_content(
                svg_element, query_event.attributes.pop("_inner_xml")
            )

        # Update the attributes of the found element
        for attr, value in query_event.attributes.items():
            # response.data[attr] = svg_element.get(attr)
            # TODO maybe we can make use of some serialisation method here rather than just using `str(...)`
            svg_element.set(attr, str(value))  # TODO handle set failures

        return response

    @staticmethod
    def _tostring(element: ET._Element, unescape: bool = True, with_tail: bool = False):
        result = ET.tostring(
            element,
            encoding=str,
            with_tail=with_tail,
        )
        if unescape:
            return html.unescape(result)
        else:
            return result

    @staticmethod
    def _stringify_children(element: ET._Element, unescape: bool = True):
        parts = [element.text] + list(
            chain(
                *(
                    [SVGApplication._tostring(c, unescape=unescape, with_tail=True)]
                    for c in element.getchildren()
                )
            )
        )
        return "".join(filter(None, parts)).strip()

    @staticmethod
    def select(
        root: ET._Element, query_event: QuerySVGEvent, unescape: bool = True
    ) -> ResponseEvent:
        """Selects and returns attributes or the entire element based on a QueryEvent,
        and returns a ResponseEvent with the selected data, converting attribute values to Python types.

        Args:
            root (Element): The root of the SVG element tree.
            query_event (QueryEvent): The query event containing select details.
            unescape (bool): whether to unescape any XML that is returned (XML that contains characters &#...;)
        Returns:
            ResponseEvent: The response event containing the selected attribute values or the element representation.
        """
        response = ResponseEvent(
            *Event.new(),
            query_event_id=query_event.id,
            success=True,
            data=dict(),
        )

        # Check if the root itself is the element to be selected
        if root.get("id", None) == query_event.element_id:
            svg_element = root
        else:
            # Find the SVG element by ID among the children
            svg_elements = root.xpath(f".//*[@id='{query_event.element_id}']")
            svg_element = svg_elements[0] if svg_elements else None

        # Check if the element exists
        if svg_element is None:
            response.success = False
            return response

        if query_event.attributes:
            # Select and convert the specified attributes
            selected_data = {
                attr: convert_attribute_value(svg_element.get(attr, None))
                for attr in query_event.attributes
            }
            # get inner xml for this element if it is a container
            if "_inner_xml" in query_event.attributes:
                if list(svg_element) or svg_element.text:
                    selected_data["_inner_xml"] = SVGApplication._stringify_children(
                        svg_element
                    )
                else:
                    # failed to set _inner_xml (it does not exist)
                    response.success = False

            # get the full xml for this element
            if "_xml" in query_event.attributes:
                selected_data["_xml"] = SVGApplication._tostring(
                    svg_element, unescape=unescape
                )
        else:
            # Convert all attributes of the element if no specific attributes are given
            selected_data = {
                key: convert_attribute_value(value)
                for key, value in svg_element.attrib.items()
            }

            if list(svg_element) or svg_element.text:
                selected_data["_inner_xml"] = SVGApplication._stringify_children(
                    svg_element
                )

        response.data = selected_data
        return response

    # @staticmethod
    # def delete(root: ET._Element, query_event: QueryRawEvent) -> ResponseEvent:
    #     """Deletes an SVG element based on the details provided in a QueryEvent instance,
    #     and returns a ResponseEvent indicating the outcome.

    #     Args:
    #         root (ET.Element): The root of the SVG element tree.
    #         query_event (QueryEvent): The query event containing delete details.

    #     Returns:
    #         ResponseEvent: The response event indicating the outcome of the delete operation.
    #     """
    #     response = ResponseEvent(
    #         *Event.new(),
    #         query_event_id=query_event.id,
    #         success=False,
    #         data=None,
    #     )

    #     # Check if the root itself is the element to be selected
    #     if root.get("id", None) == query_event.element_id:
    #         svg_element = root
    #     else:
    #         # Find the SVG element by ID among the children
    #         svg_elements = root.xpath(f".//*[@id='{query_event.element_id}']")
    #         svg_element = svg_elements[0] if svg_elements else None

    #     # Check if the element exists
    #     if svg_element is None:
    #         return response

    #     svg_element = svg_elements[0]
    #     parent = svg_element.getparent()
    #     if parent is not None:
    #         parent.remove(svg_element)
    #         response.success = True

    #     return response

    @property
    def width(self):
        return int(self.element_tree_root.get("width"))

    @property
    def height(self):
        return int(self.element_tree_root.get("height"))


def replace_element_content(original_element, new_content):
    for child in original_element.getchildren():
        original_element.remove(child)
    # Parse the new content
    new_elements = ET.fromstring(f"<_dummy> {new_content} </_dummy>")
    # Append new elements to <g>
    for new_child in new_elements.getchildren():
        original_element.append(new_child)
    # If there's text in the new content, append it as well
    if new_elements.text:
        original_element.text = new_elements.text


def convert_attribute_value(value: str):
    """Converts a string attribute value to an appropriate Python type using ast.literal_eval."""
    try:
        # Safely evaluate value as a Python literal
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # Return the original value if it's not a valid Python literal
        return value
