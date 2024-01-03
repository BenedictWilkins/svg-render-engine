""" This package defines the PygameSVGEngine class. """
import sys
import pygame

from .event import _EventFactory


class PygameSVGEngine:
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

            if self.event_callback and events:
                self.event_callback(events)

            self.screen.fill((0, 0, 0))  # Fill the screen with black color
            pygame.display.flip()  # Update the full display Surface to the screen

        pygame.quit()
        sys.exit()
