import unittest


class TestSVGApplication(unittest.TestCase):
    def test_init_error(self):
        from svgrenderengine.engine import SVGApplication

        try:
            app = SVGApplication()
        except:
            pass

    ## TEST SELECT ##

    def test_select_element_attr(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "myrect"
        ATTR = "width"
        ATTR_VALUE = (
            200  # this should be an int! query will convert to primitive python types
        )
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <!-- Background rectangle -->
            <rect id="{ID}" {ATTR}="{ATTR_VALUE}" height="320" fill="#f5f5f5" />
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=[ATTR]
        )
        result = app.query(query)
        self.assertEqual(result.data, {ATTR: ATTR_VALUE})

    def test_select_element_attrs(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "myrect"
        ATTR1 = "width"
        ATTR1_VALUE = (
            200  # this should be an int! query will convert to primitive python types
        )
        ATTR2 = "height"
        ATTR2_VALUE = (
            100  # this should be an int! query will convert to primitive python types
        )
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <!-- Background rectangle -->
            <rect id="{ID}" {ATTR1}="{ATTR1_VALUE}" {ATTR2}="{ATTR2_VALUE}" fill="#f5f5f5" />
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=[ATTR1, ATTR2]
        )
        result = app.query(query)
        self.assertEqual(result.data, {ATTR1: ATTR1_VALUE, ATTR2: ATTR2_VALUE})

    def test_select_element(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "mygroup"
        TEMPLATE_VAR = "{{template_variable}}"
        INNER_TEXT = "some text"
        INNER_XML_ELEMENT = """<rect width="100" height="100"/>"""
        INNER = f"""{TEMPLATE_VAR}\n{INNER_TEXT}\n{INNER_XML_ELEMENT}\n"""
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <rect id="myrect" width="200" height="320" fill="#f5f5f5" />
            <g id="{ID}" stroke-width="1">{INNER}</g>
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=None
        )
        result = app.query(query)
        self.assertIn("_inner_xml", result.data)
        self.assertIn("id", result.data)
        self.assertIn("stroke-width", result.data)
        self.assertIn(INNER_TEXT, result.data["_inner_xml"])
        self.assertIn(INNER_TEXT, result.data["_inner_xml"])
        self.assertIn("<rect", result.data["_inner_xml"])

    def test_select_inner_xml(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "mygroup"
        TEMPLATE_VAR = "{{template_variable}}"
        INNER_TEXT = "some text"
        INNER_XML_ELEMENT = """<rect width="100" height="100"/>"""
        INNER = f"""{TEMPLATE_VAR}\n{INNER_TEXT}\n{INNER_XML_ELEMENT}\n"""
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <rect id="myrect" width="200" height="320" fill="#f5f5f5" /> test_head
            <g id="{ID}" stroke-width="1">{INNER}</g> test_tail
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=["_inner_xml"]
        )
        result = app.query(query)
        self.assertDictEqual(
            result.data,
            {
                "_inner_xml": '{{template_variable}}\nsome text\n<rect xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine" width="100" height="100"/>'
            },
        )

    def test_select_element_xml(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "mygroup"
        TEMPLATE_VAR = "{{template_variable}}"
        INNER_TEXT = "some text"
        INNER_XML_ELEMENT = """<rect width="100" height="100"/>"""
        INNER = f"""{TEMPLATE_VAR}\n{INNER_TEXT}\n{INNER_XML_ELEMENT}\n"""
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <rect id="myrect" width="200" height="320" fill="#f5f5f5" />
            test-head
            <g id="{ID}" stroke-width="1">{INNER}</g>test-tail
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=["_xml"]
        )
        result = app.query(query)
        self.assertIn("_xml", result.data)
        self.assertIn(ID, result.data["_xml"])
        self.assertIn(INNER_TEXT, result.data["_xml"])
        self.assertIn(INNER_TEXT, result.data["_xml"])
        self.assertIn("<rect", result.data["_xml"])
        self.assertNotIn("test-head", result.data["_xml"])
        self.assertNotIn("test-tail", result.data["_xml"])

    ## TEST UPDATE ##

    def test_update_element_attr(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "myrect"
        ATTR = "width"
        ATTR_VALUE = (
            200  # this should be an int! query will convert to primitive python types
        )
        ATTR_NEW_VALUE = 100
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <!-- Background rectangle -->
            <rect id="{ID}" {ATTR}="{ATTR_VALUE}" height="320" fill="#f5f5f5" />
            </svg>
        """
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.UPDATE, element_id=ID, attributes={ATTR: ATTR_NEW_VALUE}
        )
        result = app.query(query)
        self.assertTrue(result.success)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=[ATTR]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertEqual(result.data[ATTR], ATTR_NEW_VALUE)

    def test_update_element_inner(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        ID = "mygroup"
        TEMPLATE_VAR = "{{template_variable}}"
        INNER_TEXT = "some text"
        INNER_XML_ELEMENT = """<rect width="100" height="100"/>"""
        INNER = f"""{TEMPLATE_VAR}\n{INNER_TEXT}\n{INNER_XML_ELEMENT}\n"""
        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
            <rect id="myrect" width="200" height="320" fill="#f5f5f5" />
            <g id="{ID}" stroke-width="1">{INNER}</g>
            </svg>
        """
        NEW_INNER_TEXT = "new text!"
        NEW_INNER_XML_ELEMENT = """<rect width="150" height="100"/>"""
        NEW_INNER = f"""{TEMPLATE_VAR}\n{NEW_INNER_TEXT}\n{NEW_INNER_XML_ELEMENT}\n"""
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.UPDATE, element_id=ID, attributes={"_inner_xml": NEW_INNER}
        )
        result = app.query(query)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id=ID, attributes=["_xml"]
        )
        result = app.query(query)
        self.assertIn(NEW_INNER_TEXT, result.data["_xml"])
        self.assertIn(NEW_INNER_XML_ELEMENT, result.data["_xml"])

    def test_update_element_inner_not_container(self):
        from svgrenderengine.engine import SVGApplication
        from svgrenderengine.event import QuerySVGEvent

        svg_code = f""" <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg">
            <rect id="myrect" width="200" height="320" fill="#f5f5f5" />
            </svg>
        """
        NEW_INNER_TEXT = "new text!"
        app = SVGApplication(svg_code=svg_code)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.UPDATE,
            element_id="myrect",
            attributes={"_inner_xml": NEW_INNER_TEXT},
        )
        result = app.query(query)
        self.assertTrue(result.success)
        query = QuerySVGEvent.create_event(
            QuerySVGEvent.SELECT, element_id="myrect", attributes=["_xml"]
        )
        result = app.query(query)
        self.assertDictEqual(
            result.data,
            {
                "_xml": '<rect xmlns="http://www.w3.org/2000/svg" id="myrect" width="200" height="320" fill="#f5f5f5"> new text! </rect>'
            },
        )


if __name__ == "__main__":
    unittest.main()
