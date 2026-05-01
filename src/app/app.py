import os
from pathlib import Path

import pygame

from config import AppConfig
from controller.simulation_controller import SimulationController


class App:
    """Main application class that initializes the simulation and runs the main loop."""

    CONFIG_PATH = Path(os.path.dirname(__file__)) / "config.toml"
    ASSETS_PATH = Path(__file__).parent / "assets"

    def __init__(self) -> None:
        """Initialize the application, including Pygame and the simulation controller."""
        pygame.init()
        self.config = AppConfig().from_file(self.CONFIG_PATH)
        self._screen = pygame.display.set_mode(
            size=(
                self.config.view.WINDOW_WIDTH,
                self.config.view.WINDOW_HEIGHT,
            )
        )
        pygame.display.set_caption("MAS Simulation")
        self._clock = pygame.time.Clock()
        self.__controller = SimulationController(
            screen=self._screen, config=self.config
        )

    def start(self) -> None:
        """Start the application."""
        while True:
            self.__controller.process_events()
            if self.__controller.done:
                break
            self.__controller.update()
            self.__controller.render()
            self._clock.tick(self.__controller.fps)
