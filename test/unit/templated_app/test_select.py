import unittest

from svgrenderengine.engine import TemplatedSVGApplication
from svgrenderengine.event import QueryEvent


class TestSVGTemplatedApplicationSelect(unittest.TestCase):
    ## TEST SELECT ##

    def test_select(self):
        svg_code = """
                    <svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> 
                        <!-- Background rectangle -->
                        <rect id="{{element.id}}" width="{{element.width}}" height="320" fill="#f5f5f5"/> 
                    </svg>
                """
        element_data = dict(element=dict(id="myrect", width=200))
        app = TemplatedSVGApplication(svg_code, element_data)

        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=["element"])
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(result.data, element_data)

    def test_select_attr(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <!-- Background rectangle --> <rect id="{{element.id}}" width="{{element.width}}" height="320" fill="#f5f5f5"/> </svg>"""
        element_data = dict(element=dict(id="myrect", width=200))
        app = TemplatedSVGApplication(svg_code, element_data)
        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=["element.width"])
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(result.data, {"element": {"width": 200}})

    def test_select_from_list_attr(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> </svg> """
        data = {"rect": {"id": "myrect", "size": [100, 200]}}
        app = TemplatedSVGApplication(svg_code, data)
        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=["rect.size[0]"])
        result = app.query(query)
        self.assertTrue(result.success)
        data_result = {"rect": {"size": {"0": 100}}}
        self.assertDictEqual(result.data, data_result)
        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=["rect.size.0"])
        result = app.query(query)
        self.assertDictEqual(result.data, data_result)

    def test_select_from_list_nested(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0.width}}" height="{{rect.size.1.height}}" fill="#f5f5f5" /> </svg> """
        data = {"rect": {"id": "myrect", "size": [{"width": 100}, {"height": 200}]}}
        app = TemplatedSVGApplication(svg_code, data)
        query = QueryEvent.create_event(
            QueryEvent.SELECT, attributes=["rect.size[0].width"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        data_result = {"rect": {"size": {"0": {"width": 100}}}}
        self.assertDictEqual(result.data, data_result)

    def test_select_all(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{id}}" width="{{value}}" height="320" fill="#f5f5f5"/> </svg>"""
        data = {"id": "myrect", "width": 200}
        app = TemplatedSVGApplication(svg_code, data)
        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=[])
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(result.data, data)

    def test_select_all_with_list_attr(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> </svg> """
        data = {"rect": {"id": "myrect", "size": [100, 200]}}
        app = TemplatedSVGApplication(svg_code, data)
        query = QueryEvent.create_event(QueryEvent.SELECT, attributes=[])
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(result.data, data)


if __name__ == "__main__":
    unittest.main()
