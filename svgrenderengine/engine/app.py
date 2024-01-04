import ast
from jinja2 import Template
from lxml import etree as ET
from ..event import QueryEvent, ResponseEvent, Event


class SVGApplication:
    def __init__(self, file=None, svg_code=None):
        if file:
            with open(file, "r") as svg_file:
                svg_code = Template(svg_file.read()).render()
        elif svg_code:
            svg_code = Template(svg_code).render()
        else:
            raise ValueError("Argument `file` or `svg_code` must be specified.")
        self.element_tree_root = ET.fromstring(svg_code)

    def query(self, query_event: QueryEvent):
        assert isinstance(query_event, QueryEvent)
        if query_event.action == QueryEvent.UPDATE:
            return SVGApplication.update(self.element_tree_root, query_event)
        elif query_event.action == QueryEvent.DELETE:
            return SVGApplication.delete(self.element_tree_root, query_event)
        elif query_event.action == QueryEvent.SELECT:
            return SVGApplication.select(self.element_tree_root, query_event)

    @staticmethod
    def update(root: ET._Element, query_event: QueryEvent) -> ResponseEvent:
        """Updates an SVG element based on the details provided in a QueryEvent instance,
        and returns a ResponseEvent indicating the outcome.

        Args:
            root (ET.Element): The root of the SVG element tree.
            query_event (QueryEvent): The query event containing update details.

        Returns:
            ResponseEvent: The response event indicating the outcome of the update operation.
        """
        # Initialize a ResponseEvent
        response = ResponseEvent(
            event=Event.create_event(),
            query_event_id=query_event.event.id,
            success=False,
            data=None,
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
            # print(f"No element found with ID {query_event.element_id}")
            return response

        svg_element = svg_elements[0]

        # Update the attributes of the found element
        for attr, value in query_event.attributes.items():
            svg_element.set(attr, value)

        # Update was successful
        response.success = True
        return response

    @staticmethod
    def delete(root: ET._Element, query_event: QueryEvent) -> ResponseEvent:
        """Deletes an SVG element based on the details provided in a QueryEvent instance,
        and returns a ResponseEvent indicating the outcome.

        Args:
            root (ET.Element): The root of the SVG element tree.
            query_event (QueryEvent): The query event containing delete details.

        Returns:
            ResponseEvent: The response event indicating the outcome of the delete operation.
        """
        response = ResponseEvent(
            event=Event.create_event(),
            query_event_id=query_event.event.id,
            success=False,
            data=None,
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
            # print(f"No element found with ID {query_event.element_id}")
            return response

        svg_element = svg_elements[0]
        # Remove the element
        parent = svg_element.getparent()
        if parent is not None:
            parent.remove(svg_element)
            response.success = True

        return response

    @staticmethod
    def select(root: ET._Element, query_event: QueryEvent) -> ResponseEvent:
        """Selects and returns attributes or the entire element based on a QueryEvent,
        and returns a ResponseEvent with the selected data, converting attribute values to Python types.

        Args:
            root (Element): The root of the SVG element tree.
            query_event (QueryEvent): The query event containing select details.

        Returns:
            ResponseEvent: The response event containing the selected attribute values or the element representation.
        """
        response = ResponseEvent(
            event=Event.create_event(),
            query_event_id=query_event.event.id,
            success=False,
            data=None,
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
            # print(f"No element found with ID {query_event.element_id}")
            return response

        if query_event.attributes:
            # Select and convert the specified attributes
            selected_data = {
                attr: convert_attribute_value(svg_element.get(attr, None))
                for attr in query_event.attributes
            }
        else:
            # Convert all attributes of the element if no specific attributes are given
            selected_data = {
                key: convert_attribute_value(value)
                for key, value in svg_element.attrib.items()
            }

        # get inner xml for this element if it is a container
        if list(svg_element) and "_inner_xml" in query_event.attributes:
            selected_data["_inner_xml"] = "".join(
                ET.tostring(child, encoding="unicode") for child in svg_element
            )

        # get the full xml for this element
        if "_xml" in query_event.attributes:
            selected_data["_xml"] = ET.tostring(svg_element, encoding="unicode")

        response.data = selected_data
        response.success = True

        return response

    @property
    def width(self):
        return int(self.element_tree_root.get("width"))

    @property
    def height(self):
        return int(self.element_tree_root.get("height"))


def convert_attribute_value(value: str):
    """Converts a string attribute value to an appropriate Python type using ast.literal_eval."""
    try:
        # Safely evaluate value as a Python literal
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # Return the original value if it's not a valid Python literal
        return value
