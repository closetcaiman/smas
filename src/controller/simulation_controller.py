"""Simulation controller."""

from typing import Tuple

import pygame

from controller.handlers.sampling import HSVImageSampler
from controller.mediator.simulation_data_bank import SimulationDataBank
from controller.mediator.simulation_mediatior import SimulationMediator
from controller.types import UserAction
from model.simulation import Simulation
from view.renderer import Renderer
from view.types import RenderContext
from view.viewport import Viewport

from . import config
from .handlers.input import InputHandler


class SimulationController:
    """Controller for managing the simulation, including the main loop, event handling, and rendering."""

    def __init__(
        self,
        screen: pygame.Surface,
        map_image_path: str,
        grid_width: int = config.DEFAULT_GRID_WIDTH,
        grid_height: int = config.DEFAULT_GRID_HEIGHT,
        num_agents: int = config.DEFAULT_AGENTS_PER_REGION,
    ) -> None:
        """
        Initialize the simulation controller.

        Args:
            screen: The Pygame surface to render on.
            map_image_path: The file path to the map image for sampling the world.
            grid_width: The width of the grid in number of cells.
            grid_height: The height of the grid in number of cells.
            num_agents: The number of agents to initialize per region.

        Returns:
            None

        """
        self.__grid_width = grid_width
        self.__grid_height = grid_height
        self.__num_agents = num_agents

        self.__world_sample = HSVImageSampler.sample_grid(
            map_image_path, grid_width, grid_height
        )

        self.__mediator = SimulationMediator(
            databank=SimulationDataBank(),
        )

        self.__simulation = Simulation(
            grid_width=grid_width,
            grid_height=grid_height,
            num_agents_per_region=num_agents,
            controller_mediator=self.__mediator,
            sample=self.__world_sample,
        )

        self.__mediator.databank.record_epoch(
            self.__simulation.world,
            self.__simulation.epoch,
        )

        self.__viewport = Viewport(
            screen=screen,
            grid_width=grid_width,
            grid_height=grid_height,
            sidebar_width=config.SIDEBAR_WIDTH,
        )

        self.__renderer = Renderer(
            viewport=self.__viewport,
            world=self.__simulation.world,
            sample=self.__world_sample,
        )

        self.__fps = config.DEFAULT_FPS
        self.__done = False
        self.__selected_cell: Tuple[int, int] | None = None
        self.__hovered_cell: Tuple[int, int] | None = None
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
        self.__last_step_time = 0

        self.__input_handler = InputHandler()

    @property
    def fps(self) -> int:
        """Get the current frames per second (FPS) for the simulation."""
        return self.__fps

    @property
    def done(self) -> bool:
        """Check if the simulation is done and should exit."""
        return self.__done

    def update(self) -> None:
        """Update the simulation state based on the current time and speed settings."""
        if self.__paused:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_step_time >= self.__step_interval:
            self.__simulation.step()
            self.__last_step_time = current_time

    def render(self) -> None:
        """Render the current state of the simulation to the screen."""
        epoch = self.__simulation.epoch
        total = self.__mediator.databank.get_total_agents(epoch)
        speed = config.SPEED_LABELS[self.__speed_index]
        self.__renderer.render(
            RenderContext(
                hovered_cell=self.__hovered_cell,
                selected_cell=self.__selected_cell,
                epoch=epoch,
                total_agents=total,
                speed_label=speed,
            )
        )
        pygame.display.flip()

    def process_events(self) -> None:
        """Process user input events and translate them into actions for the simulation."""
        for action, data in self.__input_handler.get_events():
            match (action, data):
                case (UserAction.QUIT, None):
                    self.__quit()
                case (UserAction.TOGGLE_PAUSE, None):
                    self.__toggle_pause()
                case (UserAction.PLACE_BARRIER, None):
                    self.__place_barrier()
                case (UserAction.SPEED_UP, None):
                    self.__speed_up()
                case (UserAction.SPEED_DOWN, None):
                    self.__speed_down()
                case (UserAction.RESET, None):
                    self.__reset()
                case (UserAction.CLICK, pos) if isinstance(pos, tuple):
                    self.__handle_click(pos)
                case (UserAction.HOVER, pos) if isinstance(pos, tuple):
                    self.__update_hover(pos)

    def __toggle_pause(self) -> None:
        """Toggle the paused state of the simulation."""
        self.__paused = not self.__paused

    def __reset(self) -> None:
        """Reset the simulation to its initial state."""
        self.__simulation = Simulation(
            grid_width=self.__grid_width,
            grid_height=self.__grid_height,
            num_agents_per_region=self.__num_agents,
            controller_mediator=self.__mediator,
            sample=self.__world_sample,
        )
        self.__renderer = Renderer(
            viewport=self.__viewport,
            world=self.__simulation.world,
            sample=self.__world_sample,
        )
        self.__selected_cell = None
        self.__hovered_cell = None
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
        self.__last_step_time = 0

    def __quit(self) -> None:
        """Set the done flag to True to exit the simulation."""
        self.__done = True

    def __place_barrier(self) -> None:
        """Place a vertical barrier in the middle column of the grid."""
        col = self.__viewport.grid_width // 2
        for region in self.__simulation.world.regions:
            if region.coordinates[0] == col:
                region.is_barrier = True

    def __speed_up(self) -> None:
        """Increase the simulation speed by decreasing the step interval."""
        if self.__speed_index < len(config.STEP_INTERVAL_MS) - 1:
            self.__speed_index += 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    def __speed_down(self) -> None:
        """Decrease the simulation speed by increasing the step interval."""
        if self.__speed_index > 0:
            self.__speed_index -= 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    def __handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle a click event at the given screen position."""
        if self.__viewport.is_in_grid_area(pos[0], pos[1]):
            cell = self.__viewport.screen_to_grid(pos[0], pos[1])
            if (
                0 <= cell[0] < self.__viewport.grid_width
                and 0 <= cell[1] < self.__viewport.grid_height
            ):
                self.__selected_cell = cell
            else:
                self.__selected_cell = None
        else:
            self.__selected_cell = None

    def __update_hover(self, pos: Tuple[int, int]) -> None:
        """Update the currently hovered cell based on the mouse position."""
        if self.__viewport.is_in_grid_area(pos[0], pos[1]):
            cell = self.__viewport.screen_to_grid(pos[0], pos[1])
            if (
                0 <= cell[0] < self.__viewport.grid_width
                and 0 <= cell[1] < self.__viewport.grid_height
            ):
                self.__hovered_cell = cell
            else:
                self.__hovered_cell = None
        else:
            self.__hovered_cell = None
