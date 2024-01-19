import unittest
from svgrenderengine.event import (
    QueryEvent,
    QuerySVGEvent,
)  # Adjust the import according to your module structure


class TestQuerySVGEvent(unittest.TestCase):
    def test_from_query_event_single_element(self):
        # Test conversion when there is only one element_id involved
        query_event = QueryEvent(
            id="test_id",
            timestamp=1234567890,
            action=QuerySVGEvent.UPDATE,
            attributes={"element1.attr1": "value1", "element1.attr2": "value2"},
        )
        result = QuerySVGEvent.from_query_event(query_event)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].element_id, "element1")
        self.assertDictEqual(
            result[0].attributes, {"attr1": "value1", "attr2": "value2"}
        )

    def test_from_query_event_multiple_elements(self):
        # Test conversion when there are multiple element_ids
        query_event = QueryEvent(
            id="test_id",
            timestamp=1234567890,
            action=QuerySVGEvent.UPDATE,
            attributes={"element1.attr1": "value1", "element2.attr1": "value2"},
        )
        result = QuerySVGEvent.from_query_event(query_event)
        self.assertEqual(len(result), 2)
        self.assertTrue(
            any(
                evt.element_id == "element1" and evt.attributes == {"attr1": "value1"}
                for evt in result
            )
        )
        self.assertTrue(
            any(
                evt.element_id == "element2" and evt.attributes == {"attr1": "value2"}
                for evt in result
            )
        )

    def test_from_query_event_list_attributes(self):
        # Test with list-type attributes
        query_event = QueryEvent(
            id="test_id",
            timestamp=1234567890,
            action=QuerySVGEvent.UPDATE,
            attributes=["element1.attr1", "element1.attr2", "element2.attr1"],
        )
        result = QuerySVGEvent.from_query_event(query_event)
        self.assertEqual(len(result), 2)
        # Finding the specific QuerySVGEvent instances for assertions
        element1_event = next(
            (evt for evt in result if evt.element_id == "element1"), None
        )
        element2_event = next(
            (evt for evt in result if evt.element_id == "element2"), None
        )

        # Assertions for element1
        self.assertIsNotNone(element1_event)
        self.assertEqual(element1_event.element_id, "element1")
        self.assertListEqual(element1_event.attributes, ["attr1", "attr2"])

        # Assertions for element2
        self.assertIsNotNone(element2_event)
        self.assertEqual(element2_event.element_id, "element2")
        self.assertListEqual(element2_event.attributes, ["attr1"])

    def test_from_query_event_invalid_attribute_format(self):
        # Test with invalid attribute format (not dot-separated)
        query_event = QueryEvent(
            id="test_id",
            timestamp=1234567890,
            action=QuerySVGEvent.UPDATE,
            attributes={"invalid_attribute": "value"},
        )
        with self.assertRaises(ValueError):
            QuerySVGEvent.from_query_event(query_event)

    def test_from_query_event_incorrect_attribute_type(self):
        # Test with incorrect attribute type (neither dict nor list)
        query_event = QueryEvent(
            id="test_id",
            timestamp=1234567890,
            action=QuerySVGEvent.UPDATE,
            attributes="invalid_attributes_type",
        )
        with self.assertRaises(ValueError):
            QuerySVGEvent.from_query_event(query_event)

    # Add more test cases as needed


if __name__ == "__main__":
    unittest.main()
