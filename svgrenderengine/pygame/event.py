import pygame

from svgrenderengine.event import (
    MouseButtonEvent,
    MouseMotionEvent,
    KeyEvent,
    ExitEvent,
    Event,
    KEY_RELEASED,
    KEY_PRESSED,
)

PYGAME_KEYDOWN = pygame.KEYDOWN
PYGAME_KEYUP = pygame.KEYUP


class _EventFactory:
    @staticmethod
    def create_exit_event_from_pygame_event(pg_event):
        assert pg_event.type == pygame.QUIT
        return ExitEvent(*Event.new())

    @staticmethod
    def create_key_event_from_pygame_event(pg_event):
        """Creates a KeyEvent instance from a Pygame keyboard event.

        Args:
            pg_event (pygame.Event): The Pygame event from which to create the KeyEvent.

        Returns:
            KeyEvent: A new instance of KeyEvent initialized with the Pygame event data.

        Raises:
            ValueError: If the provided Pygame event is not a KEYDOWN or KEYUP event.
        """
        if pg_event.type not in (PYGAME_KEYDOWN, PYGAME_KEYUP):
            raise ValueError(
                "The provided Pygame event is not a KEYDOWN or KEYUP event."
            )

        status = KEY_PRESSED if pg_event.type == PYGAME_KEYDOWN else KEY_RELEASED
        return KeyEvent(
            *Event.new(),
            key=pg_event.key,
            key_name=pygame.key.name(pg_event.key),
            status=status,
        )

    @staticmethod
    def create_mouse_button_event_from_pygame_event(pg_event):
        """
        Creates a MouseButtonEvent instance from a Pygame mouse event.

        Args:
            pg_event (pygame.Event): The Pygame event from which to create the MouseEvent.
            clickable_elements (List[xml.Element]): A list of clickable elements in the SVG.

        Returns:
            MouseEvent: A new instance of MouseEvent initialized with the Pygame event data.

        Raises:
            ValueError: If the provided Pygame event is not a MOUSEBUTTONDOWN or MOUSEBUTTONUP event.
        """
        if pg_event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            raise ValueError(
                "The provided Pygame event is not a MOUSEBUTTONDOWN or MOUSEBUTTONUP event."
            )

        status = "pressed" if pg_event.type == pygame.MOUSEBUTTONDOWN else "released"
        return MouseButtonEvent(
            *Event.new(),
            button=pg_event.button,
            position=pg_event.pos,
            status=status,
        )

    @staticmethod
    def create_mouse_motion_event_from_pygame_event(pg_event):
        """
        Creates a MouseMoveEvent instance from a Pygame mouse movement event.

        Args:
            pg_event (pygame.Event): The Pygame event from which to create the MouseMoveEvent.

        Returns:
            MouseMoveEvent: A new instance of MouseMoveEvent initialized with the Pygame event data.

        Raises:
            ValueError: If the provided Pygame event is not a MOUSEMOTION event.
        """
        if pg_event.type != pygame.MOUSEMOTION:
            raise ValueError("The provided Pygame event is not a MOUSEMOTION event.")

        return MouseMotionEvent(
            *Event.new(), position=pg_event.pos, relative=pg_event.rel
        )
