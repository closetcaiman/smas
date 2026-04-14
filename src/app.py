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
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(
            (
                DEFAULT_WINDOW_WIDTH,
                DEFAULT_WINDOW_HEIGHT,
            )
        )
        pygame.display.set_caption("MAS Simulation")
        self._clock = pygame.time.Clock()

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    @property
    def clock(self) -> pygame.time.Clock:
        return self._clock

    def quit(self) -> None:
        pygame.quit()


def main() -> None:
    app = App()
    controller = SimulationController(
        screen=app.screen,
        grid_width=DEFAULT_GRID_WIDTH,
        grid_height=DEFAULT_GRID_HEIGHT,
        num_agents=DEFAULT_AGENTS_PER_REGION,
        map_image_path=os.path.join(
            os.path.dirname(__file__), "assets/sample-map-1.png"
        ),
    )

    while True:
        controller.process_events()
        if controller.done:
            break
        controller.update()
        controller.render()
        app.clock.tick(controller.fps)

    app.quit()


if __name__ == "__main__":
    main()
