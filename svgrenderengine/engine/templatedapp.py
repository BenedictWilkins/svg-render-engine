import copy
import logging
from jinja2 import Environment, Undefined
from omegaconf import OmegaConf, DictConfig
from lxml import etree as ET

from ..event import QueryEvent, ResponseEvent, QuerySVGEvent
from .svgapp import SVGApplication

LOGGER = logging.getLogger("svg-render-engine")

VARIABLE_OPEN = "\u01B5"  # "_\uE300"
VARIABLE_CLOSE = "\u01B6"  # "_\uE301"


class UndefinedWithError(Undefined):
    def __str__(self):
        raise ValueError(f"template variable {self._undefined_name} was not defined.")


class UndefinedReplace(Undefined):
    def __str__(self):
        return f"{{{{{self._undefined_name}}}}}"


def _xml_compat(fun):
    def decorator(self, query_event: QueryEvent):
        query_event = self._xml_compatible_query_event(query_event)
        response_event = fun(self, query_event)
        return self._xml_compatible_response_event(response_event)

    return decorator


class TemplatedSVGApplication:
    def __init__(
        self,
        templated_svg_code,
        variables,
        variable_open=r"{{",
        variable_close=r"}}",
    ):
        super().__init__()
        self._variable_open = variable_open
        self._variable_close = variable_close

        self._internal_variable_open = VARIABLE_OPEN
        self._internal_variable_close = VARIABLE_CLOSE

        self._environment = Environment(
            undefined=UndefinedWithError,
            variable_start_string=self._variable_open,
            variable_end_string=self._variable_close,
        )
        self._variables = OmegaConf.create(copy.deepcopy(variables))
        self._template_root = ET.fromstring(self._preprocess_xml(templated_svg_code))

    def render_template(self):
        template = ET.tostring(
            self._template_root, encoding="unicode", pretty_print=True
        )
        return self._postprocess_xml(template)

    def render(self):
        return TemplatedSVGApplication._render(
            self._environment, self._template_root, self._variables
        )

    @staticmethod
    def _render(
        environment: Environment, template_root: ET._Element, variables: DictConfig
    ):
        return environment.from_string(
            ET.tostring(template_root, encoding="unicode", pretty_print=True)
        ).render(**OmegaConf.to_container(variables))

    def _query_template_select(self, query_event: QueryEvent):
        pass  # TODO check which query attributes contain template code, cache them, and make xml compatible.
        # use the cache to convert response data back to default template structure.

    def query(self, query_event: QueryEvent):
        # this will ensure that the event uses proper template delimiters...
        # TODO an option to turn this off? its a bit expensive? better that the events are created with the correct delimiters?
        if isinstance(query_event, QueryEvent):
            if query_event.action == QueryEvent.UPDATE:
                return TemplatedSVGApplication.update(self._variables, query_event)
            elif query_event.action == QueryEvent.SELECT:
                return TemplatedSVGApplication.select(self._variables, query_event)
            elif query_event.action == QueryEvent.UPDATE_TEMPLATE:
                return TemplatedSVGApplication.update_template(
                    self._template_root, query_event
                )
            elif query_event.action == QueryEvent.SELECT_TEMPLATE:
                return self.select_template(query_event)
            elif query_event.action == QueryEvent.SELECT_RENDERED:
                return TemplatedSVGApplication.select_rendered(
                    self._environment, self._template_root, self._variables, query_event
                )
            else:
                raise ValueError(
                    f"Received unknown action {query_event.action} in {query_event}"
                )
        else:
            raise ValueError(f"Received unknown Event type {type(query_event)}")

    @staticmethod
    def update(variables: DictConfig, query_event: QueryEvent):
        """Update `variables` using the `attributes` present in `query_event`. Each key in `query_event.attributes` should be a dot seperated key to the variable that should be updated.

        Args:
            variables ([DictConfig]): variables to be updated.
            query_event ([QueryEvent]): query containing update data.
        """
        # Initialize a ResponseEvent
        response = ResponseEvent.create_event(
            query_event_id=query_event.id,
            success=True,
            data=dict(),  # TODO do we want to return the old values that were updated? is there any reason to?
        )
        for attr, value in query_event.attributes.items():
            # TODO try except
            OmegaConf.update(variables, attr, value)
        return response

    @staticmethod
    def select(variables: DictConfig, query_event: QueryEvent):
        """Select `variables` using the attributes present in `query_event`. Each key in `query_event.attributes` should be a dot seperated key to the variable that should be selected.

        Args:
            variables ([DictConfig]): variables to be selected.
            query_event ([QueryEvent]): query containing select keys.
        """

        if len(query_event.attributes) == 0:
            return ResponseEvent.create_event(
                query_event_id=query_event.id,
                success=True,
                data=OmegaConf.to_container(variables),
            )
        else:
            data = OmegaConf.create()
            try:
                for attr in query_event.attributes:
                    # TODO support slice accessing? e.g. a.b[:2] assuming a.b is a list...
                    OmegaConf.update(
                        data, attr, OmegaConf.select(variables, attr), force_add=True
                    )
            except KeyError as e:
                return ResponseEvent.create_event(
                    query_event_id=query_event.id, success=False, data=dict(error=e)
                )
            return ResponseEvent.create_event(
                query_event_id=query_event.id,
                success=True,
                data=OmegaConf.to_container(data),
            )

    @staticmethod
    def update_template(
        template_root: ET._Element, query_event: QueryEvent | QuerySVGEvent
    ):
        """Update the SVG (or XML) template that represents this application using the `attributes` in `query_event`. Each key in `query_event.attributes` should be a dot seperated key to the variable in the SVG template that should be updated.
        This update accepts two kinds of `Query`:
            [QueryEvent] : The first value in the dot-seperated key in `query_event.attributes` (e.g. "id.attribute") is treated as the XML element `id` tag, the second is the XML element tag value to update. For example: a key value pair ("myrect.width" : 100) on an XML element `<rect id="myrect" width=""200" />` will update to `<rect id="myrect", width="100" />`. Internally a [QueryEvent] is converted to a collection of [QuerySVGEvent]s.

            [QuerySVGEvent] : TODO

        Notes:
            This update is over the template, not the final XML/SVG that is resolved using variables. This means that it is common to use key/value pairs that contain template code, for example to update:

            `<rect id="{{myrect.id}}" width="{{myrect.width}}" height="{{myrect.height}}"/>`

            A query such as:

            ```
                QueryEvent.create_event(QueryEvent.UPDATE_TEMPLATE, attributes={
                    "{{myrect.id}}.id"       : "rectangle-001",
                    "{{myrect.width}}.width" : 100
                })
            ```

            will modify the values associated with the `id` and `width` tags, the result being:

            `<rect id="rectangle-001" width="100" height="{{myrect.height}}"/>`

            Notice that any `.` inside the template block `{{ }}` will be treated as part of the tag value so that the element can be properly resolved.

            It is quite easy to make a state variable obsolete by directly modifying the template. The variable `myrect.width` is now unused in the template, but may still be present in the state (i.e. on [TemplatedSVGApplication.select] and [TemplatedSVGApplication.update]). TODO may this should not be so?
        Args:
            template_root (ET._Element): the root of the SVG template in use.
            query_event (QueryEvent): the query used to update the SVG template.

        Returns:
            [ResponseEvent]: the response event generated by the query.
        """
        assert isinstance(query_event, QueryEvent)  # TODO allow QuerySVGEvent

        svg_events = QuerySVGEvent.from_query_event(query_event)
        response_success = True
        response_data = {}
        for svg_event in svg_events:
            response = SVGApplication.update(template_root, svg_event)
            response_success &= response.success
            response_data = {
                f"{svg_event.element_id}.{key}": value
                for key, value in response.data.items()
            }
        # gathered responses...
        return ResponseEvent.create_event(
            query_event_id=query_event.id, success=response_success, data=response_data
        )

    def select_template(self, query_event: QueryEvent | QuerySVGEvent):
        if isinstance(query_event, QuerySVGEvent):
            query_event = self._xml_compatible_query_svg_event(query_event)
            # TODO test this
            return self._xml_compatible_response_event(
                SVGApplication.select(self._template_root, query_event)
            )
        elif isinstance(query_event, QueryEvent):
            query_event = self._xml_compatible_query_event(query_event)
            # split this query_event into many QuerySVGEvents
            svg_events = QuerySVGEvent.from_query_event(
                query_event, self._internal_variable_open, self._internal_variable_close
            )
            response_success = True
            response_data = {}
            for svg_event in svg_events:
                post_element_id = self._postprocess_xml(svg_event.element_id)
                response = SVGApplication.select(self._template_root, svg_event)
                response_success &= response.success
                response_data[post_element_id] = {}
                for key, value in response.data.items():
                    response_data[post_element_id][
                        self._postprocess_xml(key)
                    ] = self._postprocess_xml(value)
            return ResponseEvent.create_event(
                query_event_id=query_event.id,
                success=response_success,
                data=response_data,
            )
        else:
            raise ValueError(f"Invalid query event type: {type(query_event)}.")

    @staticmethod
    def select_rendered(
        environment: Environment,
        template_root: ET._Element,
        variables: DictConfig,
        query_event: QueryEvent | QuerySVGEvent,
    ):
        """Selects svg content from the fully rendered svg code associated with this application. This call is relatively expensive as it requires a full resolution of the template with all application state variables. TODO implement some kind of caching of the fully rendered SVG code?

        TODO document what query_event is doing here.
        TODO allow QuerySVGEvent

        Args:
            query_event (QueryEvent): query event to use.

        Returns:
            List[ResponseEvent]: the responses for each query event.
        """
        svg_root = TemplatedSVGApplication._render(
            environment, template_root, variables
        )
        assert (
            query_event.attributes
        )  # TODO perhaps if empty this should select all attributes of all elements?
        assert isinstance(query_event, QueryEvent)  # TODO allow QuerySVGEvent

        svg_events = QuerySVGEvent.from_query_event(query_event)
        response_success = True
        response_data = {}
        for svg_event in svg_events:
            response = SVGApplication.select(svg_root, svg_event)
            response_success &= response.success
            response_data.update(
                {
                    f"{svg_event.element_id}.{key}": value
                    for key, value in response.data.items()
                }
            )
        # gathered responses...
        return ResponseEvent.create_event(
            query_event_id=query_event.id,
            success=response_success,
            data=response_data,
        )

    @staticmethod
    def _process_xml(value, open, close, replace_open, replace_close):
        value = value.replace(open, replace_open)
        value = value.replace(close, replace_close)
        return value

    def _preprocess_xml(self, value):
        if isinstance(value, str):
            return TemplatedSVGApplication._process_xml(
                value,
                self._variable_open,
                self._variable_close,
                self._internal_variable_open,
                self._internal_variable_close,
            )
        else:
            return value

    def _postprocess_xml(self, value):
        if isinstance(value, str):
            return TemplatedSVGApplication._process_xml(
                value,
                self._internal_variable_open,
                self._internal_variable_close,
                self._variable_open,
                self._variable_close,
            )
        else:
            return value

    def _xml_compatible_query_svg_event(self, query_event: QuerySVGEvent):
        """This function will convert the `attributes` of the given `query_event` to an xml compatible format.

        Args:
            query_event (QuerySVGEvent) : query event to make xml compatible.
        Returns:
            QuerySVGEvent: `query_event`, but with xml compatible `attributes`.
        """
        query_event.element_id = self._preprocess_xml(query_event.element_id)
        return self._xml_compatible_query_event(query_event)

    def _xml_compatible_response_event(self, response_event: ResponseEvent):
        new_data = {
            self._postprocess_xml(k): self._postprocess_xml(v)
            for k, v in response_event.attributes.items()
        }
        response_event.data = new_data
        return response_event

    def _xml_compatible_query_event(self, query_event: QueryEvent):
        """This function will convert the `attributes` of the given `query_event` to an xml compatible format.

        Args:
            query_event (QueryEvent) : query event to make xml compatible.
        Returns:
            QueryEvent: `query_event`, but with xml compatible `attributes`.
        """
        new_attributes = None
        if isinstance(query_event.attributes, dict):
            new_attributes = {
                self._preprocess_xml(k): self._preprocess_xml(v)
                for k, v in query_event.attributes.items()
            }
            query_event.attributes = new_attributes
        elif isinstance(query_event.attributes, list):
            new_attributes = [self._preprocess_xml(x) for x in query_event.attributes]
            query_event.attributes = new_attributes
        else:
            raise ValueError(
                f"Invalid type for {QueryEvent.__name__} attributes: {type(query_event.attributes)}, must be list or dict."
            )
        return query_event

    @staticmethod
    def _get_dot_keys(config, parent_key=""):
        """Recursively fetch keys from DictConfig in dot-separated format.

        Args:
            config (DictConfig): The DictConfig object to traverse.
            parent_key (str): The base key for the current level of recursion. Defaults to an empty string.

        Returns:
            list: A list of dot-separated keys representing paths through the DictConfig.
        """
        keys = []
        for k, v in config.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, DictConfig):
                keys.extend(TemplatedSVGApplication._get_dot_keys(v, full_key))
            else:
                keys.append(full_key)
        return keys

    # def _get_all_variables(self, env, template_source):
    #     ast = env.parse(template_source)

    #     def recurse_getattr(g: Getattr):
    #         # if isinstance(g.node, Name):
    #         #    return g.node.name
    #         if isinstance(g.node, Getattr):
    #             return recurse_getattr(g.node) + "." + g.attr
    #         return g.node.name + "." + g.attr

    #     all_fields = set()
    #     to_remove = set(env.globals.keys())

    #     for g in ast.find_all(Getattr):
    #         all_fields.add(recurse_getattr(g))
    #     for g in ast.find_all(Name):
    #         all_fields.add(g.name)

    #     all_fields = all_fields.difference(to_remove)
    #     return all_fields


# def _postprocess_xml(root, replace_open, replace_close):
#     # TODO unused? it wont work to convert the XML tree...
#     for element in root.iter():
#         if isinstance(element.tag, str):
#             # Revert element and attribute names back to original
#             # print("TAG", element.tag, type(element.tag))

#             element.tag = element.tag.replace(replace_open, r"{{").replace(
#                 replace_close, r"}}"
#             )
#             for attr in element.attrib:
#                 new_attr = attr.replace(replace_open, r"{{").replace(
#                     replace_close, r"}}"
#                 )
#                 if new_attr != attr:
#                     element.attrib[new_attr] = element.attrib.pop(attr)
#         else:
#             LOGGER.debug(
#                 "Skipping xml template post processing on tag: %s as it is not a `str`.",
#                 str(element.tag),
#             )


def _xml_compatible_replace(
    variable,
    variable_open,
    variable_close,
    default_variable_open,
    default_variable_close,
):
    variable = variable.replace(default_variable_open, variable_open)
    variable = variable.replace(default_variable_close, variable_close)
    return variable


if __name__ == "__main__":
    template_source = """
            {% for j in range(0, 4) %}
                <!-- Vertical rectangle -->
                <rect id="slider-{{j}}" x="{{ 10 + j * 50 }}" y="70" width="30" height="220" fill="#add9e6" svgre:clickable="true"/>
            {% endfor %}"""
    app = TemplatedSVGApplication(template_source, dict(a=1, b=2, c=3))
