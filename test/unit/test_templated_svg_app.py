import unittest

from svgrenderengine.engine import TemplatedSVGApplication
from svgrenderengine.event import QueryEvent


class TestSVGTemplatedApplication(unittest.TestCase):
    ## TEST SELECT ##

    def test_select_rendered_xml(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        app = TemplatedSVGApplication(
            svg_code,
            {
                "rect": {"id": "myrect", "size": [100, 200]},
                "group": {"id": "mygroup", "inner": "hello world"},
            },
        )
        query = QueryEvent.create_event(
            QueryEvent.SELECT_RENDERED, attributes=["root._xml"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {
                "root._xml": '<svg xmlns="http://www.w3.org/2000/svg" id="root" width="200" height="320"> <rect id="myrect" width="100" height="200" fill="#f5f5f5"/> <g id="mygroup" stroke-width="1"> hello world </g> </svg>'
            },
        )

    def test_select_rendered_inner_xml(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        app = TemplatedSVGApplication(
            svg_code,
            {
                "rect": {"id": "myrect", "size": [100, 200]},
                "group": {"id": "mygroup", "inner": "hello world"},
            },
        )
        query = QueryEvent.create_event(
            QueryEvent.SELECT_RENDERED, attributes=["mygroup._inner_xml"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(result.data, {"mygroup._inner_xml": "hello world"})

    def test_select_rendered_all(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        app = TemplatedSVGApplication(
            svg_code,
            {
                "rect": {"id": "myrect", "size": [100, 200]},
                "group": {"id": "mygroup", "inner": "hello world"},
            },
        )
        query = QueryEvent.create_event(
            QueryEvent.SELECT_RENDERED, attributes=["myrect", "mygroup"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            {
                "myrect.id": "myrect",
                "myrect.width": 100,
                "myrect.height": 200,
                "myrect.fill": "#f5f5f5",
                "mygroup.id": "mygroup",
                "mygroup.stroke-width": 1,
                "mygroup._inner_xml": "hello world",
            },
        )

    def test_select_rendered_everything(self):
        pass  # TODO? select the attributes of all elements?

    def test_update_attrs(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        app = TemplatedSVGApplication(
            svg_code,
            {
                "rect": {"id": "myrect", "size": [100, 200]},
                "group": {"id": "mygroup", "inner": "hello world"},
            },
        )
        NEW_ATTRS = {"group.inner": "hello new world!", "rect.id": "myrect2"}
        query = QueryEvent.create_event(QueryEvent.UPDATE, attributes=NEW_ATTRS)
        result = app.query(query)
        self.assertTrue(result.success)
        query = QueryEvent.create_event(
            QueryEvent.SELECT, attributes=["group.inner", "rect.id"]
        )
        result = app.query(query)
        self.assertTrue(result.success)
        self.assertDictEqual(
            result.data,
            NEW_ATTRS,
        )

    def test_update_template_attrs(self):
        svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        app = TemplatedSVGApplication(
            svg_code,
            {
                "rect": {"id": "myrect", "size": [100, 200]},
                "group": {"id": "mygroup", "inner": "hello world"},
            },
        )
        query = QueryEvent.create_event(
            QueryEvent.UPDATE_TEMPLATE, attributes={"{{group.id}}.id": "new_group"}
        )
        result = app.query(query)
        self.assertTrue(result.success)
        query = QueryEvent.create_event(
            QueryEvent.SELECT_RENDERED,
            attributes=["root._xml"],
        )
        result = app.query(query)
        print(result)
        # self.assertTrue(result.success, "failed to get updated id 'new_group'")
        # self.assertDictEqual(
        #     result.data,
        # )


if __name__ == "__main__":
    unittest.main()
