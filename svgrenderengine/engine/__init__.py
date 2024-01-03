from ..pygame import PygameView


from .query import find_all_clickable_elements


class SVGRenderEngine:
    def __init__(self, svg):
        self.state = svg  # we could translate it first?
        self._view = PygameView(
            # event_callback=self.svg_event_callback
        )  # by default (TODO change)

    def run(self):
        self._view.run()
