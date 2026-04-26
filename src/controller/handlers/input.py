from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, cast

import pygame

from controller.types import UserAction

if TYPE_CHECKING:
    pass


class InputHandler:
    """Translates Pygame events into high-level commands."""

    def __init__(self) -> None:
        """Initialize the input handler, including key mappings and state variables."""
        self.__key_map = {
            pygame.K_ESCAPE: UserAction.QUIT,
            pygame.K_q: UserAction.QUIT,
            pygame.K_SPACE: UserAction.TOGGLE_PAUSE,
            pygame.K_r: UserAction.RESET,
            pygame.K_b: UserAction.PLACE_BARRIER,
            pygame.K_UP: UserAction.SPEED_UP,
            pygame.K_DOWN: UserAction.SPEED_DOWN,
        }

    def get_events(self):
        """Yield actions, clicks, or mouse movements."""
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    yield (UserAction.QUIT, None)
                case pygame.KEYDOWN:
                    if action := self.__key_map.get(event.key):
                        yield (action, None)
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        pos = cast(Tuple[int, int], event.pos)
                        if pos is not None:
                            yield (UserAction.CLICK, pos)
                case pygame.MOUSEMOTION:
                    pos = cast(Tuple[int, int], event.pos)
                    if pos is not None:
                        yield (UserAction.HOVER, pos)
