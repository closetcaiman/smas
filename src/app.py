import os

import pygame

from controller.config import (
    DEFAULT_AGENTS_PER_REGION,
    DEFAULT_GRID_HEIGHT,
    DEFAULT_GRID_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
)
from controller.simulation_controller import SimulationController


class App:
    """Main application class that initializes the simulation and runs the main loop."""

    def __init__(self) -> None:
        """Initialize the application, including Pygame and the simulation controller."""
        pygame.init()
        self._screen = pygame.display.set_mode(
            size=(
                DEFAULT_WINDOW_WIDTH,
                DEFAULT_WINDOW_HEIGHT,
            )
        )
        pygame.display.set_caption("MAS Simulation")
        self._clock = pygame.time.Clock()
        self.__conroller = SimulationController(
            screen=self._screen,
            grid_width=DEFAULT_GRID_WIDTH,
            grid_height=DEFAULT_GRID_HEIGHT,
            num_agents=DEFAULT_AGENTS_PER_REGION,
            map_image_path=os.path.join(
                os.path.dirname(__file__), "assets/sample-map-1.png"
            ),
        )

    def start(self) -> None:
        """Start the application."""
        while True:
            self.__conroller.process_events()
            if self.__conroller.done:
                break
            self.__conroller.update()
            self.__conroller.render()
            self._clock.tick(self.__conroller.fps)
