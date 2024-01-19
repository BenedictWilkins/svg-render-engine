from .query import *
from .svgapp import SVGApplication
from .templatedapp import TemplatedSVGApplication

ENGINE_NAMESPACE = 'xmlns:svgre="svg_render_engine"'


def load_svg_as_element_tree(file):
    with open(file, "r") as svg_file:
        svg_code = svg_file.read()
        return resolve_templated_svg_as_element_tree(svg_code)


def resolve_templated_svg_as_element_tree(svg_code):
    from jinja2 import Template
    import xml.etree.ElementTree as ET

    svg_code = Template(svg_code).render()
    element_tree_root = ET.fromstring(svg_code)
    width = int(element_tree_root.get("width"))
    height = int(element_tree_root.get("height"))

    return element_tree_root, dict(width=width, height=height)
