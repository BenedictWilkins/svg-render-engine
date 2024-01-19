import xml.etree.ElementTree as ET

from svgrenderengine.engine.query import find_all_clickable_elements


# Example SVG code
svg_code = """
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" xmlns:svgre="svg_render_engine">
    <!-- A clickable rectangle with optimized speed -->
    <rect x="10" y="10" width="50" height="50" fill="red" id="myrect" svgre:clickable="true"/>
    <!-- A circle with crisp edges -->
    <circle cx="100" cy="50" r="40" fill="green" id="mycircle"/>
</svg>
"""

# Extract clickable elements
element_tree_root = ET.fromstring(svg_code)
clickables = find_all_clickable_elements(element_tree_root)

# Output the result (for demonstration purposes)
for elem in clickables:
    print(ET.tostring(elem, encoding="unicode"))
    print(elem.attrib.get("id"))
