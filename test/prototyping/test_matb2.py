if __name__ == "__main__":
    from svgrenderengine.pygame import PygameView
    from svgrenderengine.event import MouseButtonEvent, ExitEvent, QuerySVGEvent, Event
    from svgrenderengine.engine.query import find_all_clickable_elements_at
    from svgrenderengine.engine import SVGApplication

    from jinja2 import Template

    from lxml import etree as ET
    import random

    def get_random_color():
        color_int = random.randint(0, 0xFFFFFF)
        color_hex = f"#{color_int:06x}"
        return color_hex

    app = SVGApplication("./test/matb2.svg")
    game = PygameView(width=app.width, height=app.height)
    # run the simulation loop
    running = True
    while running:
        for event in game.step():
            result = app.query(
                QuerySVGEvent(*Event.new(), QuerySVGEvent.SELECT, "root", ["_xml"])
            )
            # print(result)

            if isinstance(event, MouseButtonEvent) and event.status == "pressed":
                elements = find_all_clickable_elements_at(
                    app.element_tree_root, event.position
                )
                for elem in elements:
                    element_id = elem.get("id")
                    # Test Update
                    # result = app.query(
                    #     QueryEvent(
                    #         *Event.new(),
                    #         QueryEvent.UPDATE,
                    #         element_id,
                    #         dict(fill=get_random_color()),
                    #     )
                    # )

                    # Test DELETE
                    # result = app.query(
                    #     QueryEvent(
                    #         *Event.new(),
                    #         QueryEvent.DELETE,
                    #         element_id,
                    #         None,
                    #     )
                    # )

                    # Test SELECT
                    result = app.query(
                        QuerySVGEvent(
                            *Event.new(),
                            QuerySVGEvent.SELECT,
                            element_id,
                            ["id", "fill", "abc"],
                        )
                    )
                    print(result)

            elif isinstance(event, ExitEvent):
                running = False
        game.render_svg(ET.tostring(app.element_tree_root, encoding="unicode"))
    game.close()
