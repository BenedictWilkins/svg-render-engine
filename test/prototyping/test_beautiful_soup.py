from lxml import etree as ET

from svgrenderengine.engine.templatedapp import TemplatedSVGApplication


svg_code = """<svg id="root" width="200" height="320" xmlns="http://www.w3.org/2000/svg"> <!-- Background rectangle --> <rect id="id" width="{{rect.size.0}}" height="{{rect.size.1}}" fill="#f5f5f5" /> </svg>"""


app = TemplatedSVGApplication(svg_code, {})


# parse
parser = ET.XMLParser(encoding="UTF-8")
root = ET.fromstring(app._preprocess_xml(svg_code), parser)
svg_element = root.xpath(".//*[@id='id']")[0]

# svg_element = app._template_root.xpath(".//*[@id='id']")[0]
import html

result = ET.tostring(svg_element, encoding="unicode", pretty_print=True)
print(result)
print(html.unescape(result))
# print(app.render_template())

# this might help!
# https://stackoverflow.com/questions/9574756/lxml-unicode-characters
