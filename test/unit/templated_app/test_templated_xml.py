import unittest


from svgrenderengine.engine.templatedapp import (
    _preprocess_xml,
    _postprocess_xml,
)


from lxml import etree as ET
from jinja2 import Environment, Template, Undefined


class TestTemplatedXMLParse(unittest.TestCase):
    def test_templated_parse_errors(self):
        xml_string = """
                    <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> 
                        <!-- Background rectangle -->
                        <{{element}} id="{{id}}" width="{{width}}" height="320" fill="#f5f5f5"/> 
                    </svg>
                    """
        with self.assertRaises(ET.XMLSyntaxError):
            ET.fromstring(xml_string)

    def test_templated_parse(self):
        xml_string = """
                    <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg">
                        <!-- Background rectangle -->
                        <{{element}} id="{{id}}" {{element.width}}="{{width}}" height="320" fill="#f5f5f5"/>
                    </svg>
                    """

        # these are the defaults
        replace_open = "_\u00C7"
        replace_close = "_\u00D8"
        xml_string = _preprocess_xml(
            xml_string, "{{", "}}", replace_open, replace_close
        )
        parser = ET.XMLParser(
            remove_comments=True,
            remove_blank_text=True,
            collect_ids=True,
        )
        root = ET.fromstring(xml_string, parser=parser)
        xml_string = ET.tostring(root)


if __name__ == "__main__":
    unittest.main()
