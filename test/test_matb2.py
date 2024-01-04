if __name__ == "__main__":
    from svgrenderengine.pygame import PygameView
    from svgrenderengine.event import MouseButtonEvent, ExitEvent
    from svgrenderengine.engine.query import find_all_clickable_elements_at
    from jinja2 import Template

    import xml.etree.ElementTree as ET
    import random

    def get_random_color():
        color_int = random.randint(0, 0xFFFFFF)
        color_hex = f"#{color_int:06x}"
        return color_hex

    ENGINE_NAMESPACE = 'xmlns:svgre="svg_render_engine"'

    with open("./test/matb2.svg", "r") as svg_file:
        svg_code = Template(svg_file.read()).render()

    element_tree_root = ET.fromstring(svg_code)
    width = int(element_tree_root.get("width"))
    height = int(element_tree_root.get("height"))
    print(width, height)

    game = PygameView(width=width, height=height)
    # run the simulation loop
    running = True
    while running:
        for event in game.step():
            if isinstance(event, MouseButtonEvent) and event.status == "pressed":
                elements = find_all_clickable_elements_at(
                    element_tree_root, event.position
                )
                print(event, elements)
                for elem in elements:
                    elem.set("fill", get_random_color())
            elif isinstance(event, ExitEvent):
                running = False
        game.render_svg(ET.tostring(element_tree_root, encoding="unicode"))
    game.close()
