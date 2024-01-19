import unittest

from svgrenderengine.engine import TemplatedSVGApplication
from svgrenderengine.event import QueryEvent


class TestSelectTemplate(unittest.TestCase):
    def test_internal_variable_block_delimiters(self):
        from svgrenderengine.engine.templatedapp import VARIABLE_OPEN, VARIABLE_CLOSE

        variable_open_old = VARIABLE_OPEN
        variable_close_cold = VARIABLE_CLOSE
        VARIABLE_OPEN = "_12345_"
        VARIABLE_CLOSE = "_abcde_"

        svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <[[rect]] id="[[id]]" prefix-[[rect.dimension]]="[[100 + rect.size.0]]" height="[[rect.size.1]]" fill="#f5f5f5" /> </svg>"""
        app = TemplatedSVGApplication(
            svg_code, {}, variable_open="[[", variable_close="]]"
        )
        pre = app._preprocess_xml(svg_code)
        post = app._postprocess_xml(pre)
        # check that the pre and post processing of [[ ]] works (metamorphic test)
        self.assertEqual(svg_code, post)

        query = QueryEvent.create_event(
            QueryEvent.SELECT_TEMPLATE,
            attributes=["[[id]].prefix-[[rect.dimension]]"],
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {"[[id]]": {"prefix-[[rect.dimension]]": "[[100 + rect.size.0]]"}},
        )
        VARIABLE_OPEN = variable_open_old
        VARIABLE_CLOSE = variable_close_cold

    def test_variable_block_delimiters(self):
        svg_code = """<svg id="root" xmlns="http://www.w3.org/2000/svg"> hello [[myworldtext]] <!-- Background rectangle --> <[[rect]] id="[[id]]" prefix-[[rect.dimension]]="[[100 + rect.size.0]]" height="[[rect.size.1]]" fill="#f5f5f5" /> </svg>"""
        app = TemplatedSVGApplication(
            svg_code, {}, variable_open="[[", variable_close="]]"
        )
        pre = app._preprocess_xml(svg_code)
        post = app._postprocess_xml(pre)
        # check that the pre and post processing of [[ ]] works (metamorphic test)
        self.assertEqual(svg_code, post)

        query = QueryEvent.create_event(
            QueryEvent.SELECT_TEMPLATE,
            attributes=["[[id]].prefix-[[rect.dimension]]"],
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {"[[id]]": {"prefix-[[rect.dimension]]": "[[100 + rect.size.0]]"}},
        )

    def test_select_template_attr(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <!-- Background rectangle --> <rect id="{{id}}" prefix-{{rect.dimension}}="{{100 + rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> </svg>"""
        app = TemplatedSVGApplication(svg_code, {})
        query = QueryEvent.create_event(
            QueryEvent.SELECT_TEMPLATE,
            attributes=["{{id}}.prefix-{{rect.dimension}}", "{{id}}.fill"],
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {
                "{{id}}": {
                    "prefix-{{rect.dimension}}": "{{100 + rect.size.0}}",
                    "fill": "#f5f5f5",
                }
            },
        )

    def test_select_template_xml(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <!-- Background rectangle --> <rect id="{{id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> </svg>"""
        app = TemplatedSVGApplication(svg_code, {})
        query = QueryEvent.create_event(
            QueryEvent.SELECT_TEMPLATE, attributes=["{{id}}._xml"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {
                "{{id}}": {
                    "_xml": '<rect xmlns="http://www.w3.org/2000/svg" id="{{id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/>'
                }
            },
        )

    def test_select_template_inner_xml(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <!-- Background rectangle --> <rect id="{{id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> test_head <g id="{{group}}" stroke-width="1"> {{some_inner_text}} <rect width="{{rect.width}}"/> {{some_other_inner_text}} </g> test_tail </svg>"""
        app = TemplatedSVGApplication(svg_code, {})
        query = QueryEvent.create_event(
            QueryEvent.SELECT_TEMPLATE, attributes=["{{group}}._inner_xml"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {
                "{{group}}": {
                    "_inner_xml": '{{some_inner_text}} <rect xmlns="http://www.w3.org/2000/svg" width="{{rect.width}}"/> {{some_other_inner_text}}'
                }
            },
        )


if __name__ == "__main__":
    unittest.main()
