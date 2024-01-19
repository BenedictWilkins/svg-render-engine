import unittest

from svgrenderengine.engine import TemplatedSVGApplication
from svgrenderengine.event import QueryEvent


class TestSVGTemplatedApplication(unittest.TestCase):
    # def test_update_template_attrs(self):
    #     svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
    #     app = TemplatedSVGApplication(
    #         svg_code,
    #         {
    #             "rect": {"id": "myrect", "size": [100, 200]},
    #             "group": {"id": "mygroup", "inner": "hello world"},
    #         },
    #     )
    #     query = QueryEvent.create_event(
    #         QueryEvent.UPDATE_TEMPLATE, attributes={"{{group.id}}.id": "new_group"}
    #     )
    #     result = app.query(query)
    #     self.assertTrue(result.success)
    #     query = QueryEvent.create_event(
    #         QueryEvent.SELECT_TEMPLATE,
    #         attributes=["new_group.id", "new_group.stroke-width"],
    #     )
    #     result = app.query(query)
    #     self.assertTrue(result.success, "failed to get updated id 'new_group'")
    #     self.assertDictEqual(
    #         result.data, {"new_group.id": "new_group", "new_group.stroke-width": 1}
    #     )

    def test_split_by_first_dot(self):
        from svgrenderengine.event.queryevent import split_by_first_dot

        # Example usage
        self.assertEqual(split_by_first_dot("{{group.id}}"), ("{{group.id}}",))
        self.assertEqual(split_by_first_dot("group"), ("group",))

        self.assertEqual(split_by_first_dot("group.id"), ("group", "id"))

        self.assertEqual(split_by_first_dot("{{group.id}}.id"), ("{{group.id}}", "id"))

        self.assertEqual(
            split_by_first_dot("Ƶgroup.idƶ.id", "Ƶ", "ƶ"),
            ("Ƶgroup.idƶ", "id"),
        )

        self.assertEqual(
            split_by_first_dot("abc{{group.id}}.id"), ("abc{{group.id}}", "id")
        )
        self.assertEqual(
            split_by_first_dot("abc{{group.id.2}}xyz.id"),
            ("abc{{group.id.2}}xyz", "id"),
        )
        self.assertEqual(
            split_by_first_dot("abc{{group.id.2,test}}{{123}}xyz.id"),
            ("abc{{group.id.2,test}}{{123}}xyz", "id"),
        )

        self.assertEqual(
            split_by_first_dot("abc.{{group.id.2,test}}{{123}}xyz.id"),
            ("abc", "{{group.id.2,test}}{{123}}xyz.id"),
        )

        # svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <rect id="{{rect.id}}" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5"/> <g id="{{group.id}}" stroke-width="1"> {{group.inner}} </g> </svg>"""
        # app = TemplatedSVGApplication(
        #     svg_code,
        #     {
        #         "rect": {"id": "myrect", "size": [100, 200]},
        #         "group": {"id": "mygroup", "inner": "hello world"},
        #     },
        # )
        # query = QueryEvent.create_event(
        #     QueryEvent.UPDATE_TEMPLATE, attributes={"{{group.id}}.id": "new_group"}
        # )
        # result = app.query(query)
        # self.assertTrue(result.success)
        # query = QueryEvent.create_event(
        #     QueryEvent.SELECT_TEMPLATE,
        #     attributes=["new_group.id", "new_group.stroke-width"],
        # )
        # result = app.query(query)
        # print(result)
        # self.assertTrue(result.success)
        # # self.assertDictEqual(
        # #     result.data,
        # # )


if __name__ == "__main__":
    unittest.main()
