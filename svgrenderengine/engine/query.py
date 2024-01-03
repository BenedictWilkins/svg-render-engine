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


def find_all_clickable_elements_at(element_tree_root, click_position):
    clickable_elements = find_all_clickable_elements(element_tree_root)
    return [
        clickable
        for clickable in clickable_elements
        if in_bounds(clickable, click_position)
    ]


def in_bounds_rect(clickable, click_position):
    x = int(clickable.get("x", 0))
    y = int(clickable.get("y", 0))
    width = int(clickable.get("width", 0))
    height = int(clickable.get("height", 0))

    click_x, click_y = click_position
    return x <= click_x <= x + width and y <= click_y <= y + height


def in_bounds_circle(clickable, click_position):
    cx = int(clickable.get("cx", 0))
    cy = int(clickable.get("cy", 0))
    r = int(clickable.get("r", 0))

    click_x, click_y = click_position
    return (click_x - cx) ** 2 + (click_y - cy) ** 2 <= r**2


def in_bounds_ellipse(clickable, click_position):
    cx = int(clickable.get("cx", 0))
    cy = int(clickable.get("cy", 0))
    rx = int(clickable.get("rx", 0))
    ry = int(clickable.get("ry", 0))

    click_x, click_y = click_position
    return ((click_x - cx) / rx) ** 2 + ((click_y - cy) / ry) ** 2 <= 1


def in_bounds(clickable, click_position):
    tag = clickable.tag.split("}")[-1]  # Get the tag name without the namespace

    if tag == "rect":
        return in_bounds_rect(clickable, click_position)
    elif tag == "circle":
        return in_bounds_circle(clickable, click_position)
    elif tag == "ellipse":
        return in_bounds_ellipse(clickable, click_position)
    else:
        # Add logic for other shapes as needed
        return False
