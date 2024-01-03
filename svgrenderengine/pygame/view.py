""" This package defines the PygameSVGEngine class. """
import sys
import io
import pygame
import cairosvg

from .event import _EventFactory


class PygameView:
    def __init__(
        self, width=640, height=480, event_callback=None, title="SVGRenderEngine"
    ):
        """
        Initializes the Pygame window.

        Args:
            width (int): Width of the window.
            height (int): Height of the window.
            event_callback (function): A callback function that is called with a list
                                       of KeyEvent objects for each keyboard event.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.event_callback = event_callback
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

    def render_svg(self, svg_code):
        """
        Renders the given SVG code in the Pygame window.

        Args:
            svg_code (str): The SVG code to be rendered.
        """
        # Convert SVG to PNG using cairosvg
        png_io = io.BytesIO()
        ANTIALIASING_SCALE = 3
        # TODO check that the svg width and height have no changed, otherwise update the pygame surface dimensions.
        cairosvg.svg2png(
            bytestring=svg_code.encode("utf-8"),
            write_to=png_io,
            output_width=ANTIALIASING_SCALE * self.width,
            output_height=ANTIALIASING_SCALE * self.height,
        )
        png_io.seek(0)
        image_surface = pygame.image.load(png_io)
        # hacky implementation of anti-aliasing as it doesnt seem to work in cairosvg
        image_surface = pygame.transform.smoothscale(
            image_surface, (self.width, self.height)
        )
        # print()
        self.screen.blit(image_surface, (0, 0))
        pygame.display.flip()

    def run(self):
        """
        Starts the main loop of the Pygame window. Listens for Pygame events and
        handles them appropriately. Calls the provided callback function with
        instances of KeyEvent and mouse event classes.
        """
        running = True
        while running:
            events = []
            for pg_event in pygame.event.get():
                if pg_event.type == pygame.QUIT:
                    running = False
                elif pg_event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    key_event = _EventFactory.create_key_event_from_pygame_event(
                        pg_event
                    )
                    events.append(key_event)
                elif pg_event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    mouse_button_event = (
                        _EventFactory.create_mouse_button_event_from_pygame_event(
                            pg_event
                        )
                    )
                    events.append(mouse_button_event)
                elif pg_event.type == pygame.MOUSEMOTION:
                    mouse_motion_event = (
                        _EventFactory.create_mouse_motion_event_from_pygame_event(
                            pg_event
                        )
                    )
                    events.append(mouse_motion_event)

            if self.event_callback:
                svg = self.event_callback(events)
                if svg:
                    self.render_svg(svg)

            # self.screen.fill((0, 0, 0))  # Fill the screen with black color
            # pygame.display.flip()  # Update the full display Surface to the screen

        pygame.quit()
        sys.exit()
