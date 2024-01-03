import xml.etree.ElementTree as ET


def find_all_clickable_elements(element_tree_root):
    # Define the namespace for 'svgre'
    namespaces = {"svgre": "svg_render_engine"}
    # Find all elements with the 'svgre:clickable' attribute
    clickable_elements = element_tree_root.findall(
        ".//*[@svgre:clickable='true']", namespaces
    )
    clickable_elements = [
        clickable
        for clickable in clickable_elements
        if clickable.attrib.get("{svg_render_engine}clickable") == "true"
    ]
    return clickable_elements


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
