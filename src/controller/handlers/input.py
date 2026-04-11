"""
Input handler - processes keyboard and mouse events.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from controller.simulation_controller import SimulationController


class InputHandler:
    """Handles keyboard and mouse input."""

    def __init__(self, ctrl: "SimulationController") -> None:
        self.__ctrl = ctrl

    def process(self) -> None:
        """Process all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__ctrl.quit()
            elif event.type == pygame.KEYDOWN:
                self.__handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.__ctrl.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.__ctrl.update_hover(event.pos)

    def __handle_key(self, key: int) -> None:
        handlers = {
            pygame.K_ESCAPE: "quit",
            pygame.K_q: "quit",
            pygame.K_SPACE: "toggle_pause",
            pygame.K_r: "reset",
            pygame.K_s: "save",
            pygame.K_b: "place_barrier",
            pygame.K_UP: "speed_up",
            pygame.K_DOWN: "speed_down",
        }
        if handler := handlers.get(key):
            getattr(self.__ctrl, handler)()
