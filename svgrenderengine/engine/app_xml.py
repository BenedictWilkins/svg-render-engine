import ast
from dataclasses import dataclass, astuple
from typing import List, Dict, Any

from svgrenderengine.event import Event

# from .app import Application
from svgrenderengine.engine.app import Application

from lxml import etree as ET
import html


@dataclass
class QueryXPath(Event):
    xpath: str
    attributes: List[str] | Dict[str, Any]

    @staticmethod
    def new(xpath: str, attributes: List[str] | Dict[str, Any]):
        return QueryXPath(*Event.new(), xpath, attributes)

    @staticmethod
    def _query(root: ET._Element, query: "QueryXPath", namespaces: Dict[str, str] = {}):
        if isinstance(query.attributes, list):
            return QueryXPath._select(root, query, namespaces=namespaces)
        elif isinstance(query.attributes, dict):
            pass  # return QueryXPath._update(root, query)
        else:
            raise ValueError(
                f"Invalid type {type(query.attributes)} for query attributes."
            )

    @staticmethod
    def _select(
        root: ET._Element, query: "QueryXPath", namespaces: Dict[str, str] = dict()
    ):
        elements = root.xpath(query.xpath, namespaces=namespaces)
        results = []
        for element in elements:
            if isinstance(element, ET._Element):
                if len(query.attributes) > 0:
                    # TODO rather than none, return a Missing object?
                    result = {
                        attrib: element.get(attrib, None) for attrib in query.attributes
                    }
                else:
                    # return the XML element itself!
                    result = _tostring(element)
            elif isinstance(element, ET._ElementUnicodeResult):
                result = str(element)
            else:
                raise ValueError(f"Unknown element type {type(element)}")

            results.append(result)
        return Response.new(query, success=True, data=results)


@dataclass
class QueryXML(QueryXPath):
    element_id: str

    @staticmethod
    def new(element_id: str, attributes: List[str] | Dict[str, Any]) -> "QueryXML":
        assert isinstance(attributes, (list, dict))
        xpath = f".//*[@id='%s']"
        return QueryXML(*astuple(QueryXPath.new(xpath, attributes)), element_id)

    @staticmethod
    def _xpath(root: ET._Element, xpath: str):
        elements = root.xpath(xpath)
        if len(elements) == 0:
            raise ValueError(f"No element was found with xpath query: {xpath}.")
        if len(elements) > 1:
            raise ValueError(
                f"More than one element was found with xpath query {xpath}, '@id' should be a unique identifier."
            )
        return elements[0]

    @staticmethod
    def _query(root: ET._Element, query: "QueryXML") -> "Response":
        if isinstance(query.attributes, list):
            return QueryXML._select(root, query)
        elif isinstance(query.attributes, dict):
            return QueryXML._update(root, query)
        else:
            raise ValueError(
                f"Invalid type {type(query.attributes)} for query attributes."
            )

    @staticmethod
    def _select(root: ET._Element, query: "QueryXML"):
        xpath = query.xpath % query.element_id
        element = QueryXML._xpath(root, xpath)
        result = {}
        # TODO select element itself!
        for key in query.attributes:
            # TODO re raise the exception?
            result[key] = _xml_to_primitive(element.get(key))
        result = {query.element_id: result}
        return Response.new(query, True, result)

    @staticmethod
    def _update(root: ET._Element, query: "QueryXML"):
        xpath = query.xpath % query.element_id
        element = QueryXML._xpath(root, xpath)
        result = {}
        for key, value in query.attributes.items():
            # TODO re raise the exception?
            result[key] = _xml_to_primitive(element.get(key))
            element.set(key, str(value))
        result = {query.element_id: result}
        return Response.new(query, True, result)


def _xml_to_primitive(value: str):
    """Converts a string attribute value to an appropriate Python type using ast.literal_eval."""
    try:
        # Safely evaluate value as a Python literal
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # Return the original value if it's not a valid Python literal
        return value


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


@dataclass
class Response(Event):
    query_id: str
    success: bool
    data: List[Any] | Dict[str, Any]

    @staticmethod
    def new(query: Event, success: bool, data: List[Any] | Dict[str, Any]):
        return Response(*Event.new(), query.id, success, data)


class XMLApplication(Application):
    def __init__(self, xml):
        self._root = ET.fromstring(xml)
        self._namespaces = {"svg": "http://www.w3.org/2000/svg"}

    def query(self, query: QueryXML):
        if isinstance(query, QueryXML):
            try:
                return QueryXML._query(self._root, query)
            except Exception as e:
                return Response.new(query, False, {"exception": e})
        elif isinstance(query, QueryXPath):
            try:
                return QueryXPath._query(self._root, query, namespaces=self._namespaces)
            except Exception as e:
                raise e  # return ResponseXML.new(query, False, {"exception": e})
        else:
            raise ValueError(f"Unknown query type: {type(query)}.")


if __name__ == "__main__":
    import unittest

    class TestXMLApplicationXPath(unittest.TestCase):
        def test_select_elements(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> <rect id="rect-1" width="100"/> <rect id="rect-2" width="200"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXPath.new("//svg:rect", [])
            result = app.query(query)
            self.assertListEqual(
                result.data,
                [
                    '<rect xmlns="http://www.w3.org/2000/svg" id="rect-1" width="100"/>',
                    '<rect xmlns="http://www.w3.org/2000/svg" id="rect-2" width="200"/>',
                ],
            )

        def test_select_text_from_element(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> <g> Some text! </g> <rect id="rect-1" width="100"/> <rect id="rect-2" width="200"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXPath.new("//svg:g/text()", [])
            result = app.query(query)
            print(result)

    class TestXMLApplication(unittest.TestCase):
        def test_select(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <rect id="[[id]]" width="[[100 + rect.size.0]]" height="[[rect.size.1]]" fill="#f5f5f5"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXML.new("[[id]]", ["width", "height"])
            result = app.query(query)
            self.assertTrue(result.success)
            self.assertDictEqual(
                result.data,
                {
                    "[[id]]": {
                        "width": "[[100 + rect.size.0]]",
                        "height": "[[rect.size.1]]",
                    }
                },
            )

        def test_select_error_id_missing(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <rect id="[[id]]" width="[[100 + rect.size.0]]" height="[[rect.size.1]]" fill="#f5f5f5"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXML.new("invalid_id", ["width", "height"])
            response = app.query(query)
            self.assertFalse(response.success)
            self.assertTrue(isinstance(response.data["exception"], Exception))

        def test_select_error_id_not_unique(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <rect id="[[id]]"/> <rect id="[[id]]"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXML.new("[[id]]", [])
            response = app.query(query)
            self.assertFalse(response.success)
            self.assertTrue(isinstance(response.data["exception"], Exception))

        def test_update(self):
            svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <rect id="[[id]]" width="[[100 + rect.size.0]]" height="[[rect.size.1]]" fill="#f5f5f5"/> </svg>"""
            app = XMLApplication(svg_code)
            query = QueryXML.new("[[id]]", {"width": 100, "height": 200})
            result = app.query(query)
            self.assertTrue(result.success)
            # result should contain the old, newly updated values
            self.assertDictEqual(
                result.data,
                {
                    "[[id]]": {
                        "width": "[[100 + rect.size.0]]",
                        "height": "[[rect.size.1]]",
                    }
                },
            )
            query = QueryXML.new("[[id]]", ["width", "height"])
            result = app.query(query)
            self.assertTrue(result.success)
            self.assertDictEqual(
                result.data,
                {
                    "[[id]]": {
                        "width": 100,
                        "height": 200,
                    }
                },
            )

    unittest.main()
