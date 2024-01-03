if __name__ == "__main__":
    from svgrenderengine.pygame import PygameView
    from svgrenderengine.event import MouseButtonEvent
    from svgrenderengine.engine.query import find_all_clickable_elements_at

    import xml.etree.ElementTree as ET
    import random

    def get_random_color():
        color_int = random.randint(0, 0xFFFFFF)
        color_hex = f"#{color_int:06x}"
        return color_hex

    ENGINE_NAMESPACE = 'xmlns:svgre="svg_render_engine"'
    WIDTH = 640
    HEIGHT = 480

    svg_code = f"""
    <svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg" {ENGINE_NAMESPACE}>
    <!-- A clickable rectangle with optimized speed -->
    <rect x="10" y="10" width="50" height="50" fill="red" id="myrect" svgre:clickable="true"/>
    <!-- A circle with crisp edges -->
    <circle cx="50" cy="50" r="40" fill="green" id="mycircle"  svgre:clickable="true"/>
    </svg>"""
    element_tree_root = ET.fromstring(svg_code)

    def callback(events):
        # Handle key events here
        for event in events:
            print(event)
            if isinstance(event, MouseButtonEvent) and event.status == "pressed":
                elements = find_all_clickable_elements_at(
                    element_tree_root, event.position
                )
                for elem in elements:
                    elem.set("fill", get_random_color())

        return ET.tostring(element_tree_root, encoding="unicode")

    game = PygameView(width=WIDTH, height=HEIGHT, event_callback=callback)
    game.run()
