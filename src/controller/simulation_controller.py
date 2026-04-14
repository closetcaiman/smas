"""
Simulation controller.
"""

from typing import TYPE_CHECKING, Tuple

import pygame

from model.map.map_image_sampler import MapImageSampler
from model.simulation.mas_stats import MASEvolutionStats
from model.simulation.simulation import Simulation

from . import config
from .handlers.data_collector import DataCollector
from .handlers.input import InputHandler
from .handlers.snapshot import SnapshotHandler

if TYPE_CHECKING:
    from view.renderer import Renderer


class SimulationController:
    def __init__(
        self,
        screen: pygame.Surface,
        map_image_path: str,
        grid_width: int = config.DEFAULT_GRID_WIDTH,
        grid_height: int = config.DEFAULT_GRID_HEIGHT,
        num_agents: int = config.DEFAULT_AGENTS_PER_REGION,
    ) -> None:
        self.__screen = screen
        self.__grid_width = grid_width
        self.__grid_height = grid_height
        self.__num_agents = num_agents
        self.__sampler = MapImageSampler(map_image_path)
        self.__sampler.sample_grid(grid_width, grid_height)

        self.__simulation = Simulation(
            grid_width, grid_height, num_agents, self.__sampler
        )
        self.__cell_size = self.__calculate_cell_size()
        self.__renderer = self.__create_renderer()
        self.__data_collector = DataCollector(self.__simulation.grid)
        self.__mas_stats = MASEvolutionStats()

        self.__fps = config.DEFAULT_FPS
        self.__done = False
        self.__selected_cell: Tuple[int, int] | None = None
        self.__hovered_cell: Tuple[int, int] | None = None
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
        self.__last_step_time = 0

        self.__input_handler = InputHandler(self)
        self.__snapshot_handler = SnapshotHandler(config.RESULTS_DIR)

    def __calculate_cell_size(self) -> int:
        grid_area_width = self.__screen.get_width() - config.SIDEBAR_WIDTH
        grid_area_height = self.__screen.get_height()
        return min(
            grid_area_width // self.__grid_width,
            grid_area_height // self.__grid_height,
        )

    def __create_renderer(self) -> "Renderer":
        from view.renderer import Renderer

        return Renderer(self.__screen, self.__simulation.grid, self.__cell_size)

    @property
    def fps(self) -> int:
        return self.__fps

    @property
    def done(self) -> bool:
        return self.__done

    def process_events(self) -> None:
        self.__input_handler.process()

    def update(self) -> None:
        if self.__paused:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_step_time >= self.__step_interval:
            self.__simulation.step()
            if self.__mas_stats.barrier_introduced:
                self.__mas_stats.calculate_stats(
                    self.__simulation.grid, self.__grid_width // 2
                )
            self.__last_step_time = current_time

    def render(self) -> None:
        epoch = self.__simulation.step_count
        total = self.__renderer.count_agents()
        speed = config.SPEED_LABELS[self.__speed_index]
        self.__renderer.render(
            self.__hovered_cell,
            self.__selected_cell,
            epoch,
            total,
            speed,
            self.__mas_stats,
        )
        pygame.display.flip()

    def toggle_pause(self) -> None:
        self.__paused = not self.__paused

    def reset(self) -> None:
        self.__simulation = Simulation(
            self.__grid_width, self.__grid_height, self.__num_agents, self.__sampler
        )
        self.__renderer = self.__create_renderer()
        self.__data_collector = DataCollector(self.__simulation.grid)
        self.__mas_stats = MASEvolutionStats()
        self.__selected_cell = None
        self.__hovered_cell = None
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
        self.__last_step_time = 0

    def save(self) -> None:
        data = self.__data_collector.collect(self.__simulation.step_count)
        self.__snapshot_handler.save(self.__simulation.step_count, data, self.__screen)

    def quit(self) -> None:
        self.__done = True

    def place_barrier(self) -> None:
        col = self.__grid_width // 2
        for row in range(self.__grid_height):
            self.__simulation.grid._data[row][col].is_barrier = True
        self.__mas_stats.record_barrier_introduction(self.__simulation.step_count, col)

    def speed_up(self) -> None:
        if self.__speed_index < len(config.STEP_INTERVAL_MS) - 1:
            self.__speed_index += 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    def speed_down(self) -> None:
        if self.__speed_index > 0:
            self.__speed_index -= 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    def handle_click(self, pos: Tuple[int, int]) -> None:
        if self.__renderer.is_in_grid_area(pos[0], pos[1]):
            cell = self.__renderer.screen_to_grid(pos[0], pos[1])
            if 0 <= cell[0] < self.__grid_width and 0 <= cell[1] < self.__grid_height:
                self.__selected_cell = cell
            else:
                self.__selected_cell = None
        else:
            self.__selected_cell = None

    def update_hover(self, pos: Tuple[int, int]) -> None:
        if self.__renderer.is_in_grid_area(pos[0], pos[1]):
            cell = self.__renderer.screen_to_grid(pos[0], pos[1])
            if 0 <= cell[0] < self.__grid_width and 0 <= cell[1] < self.__grid_height:
                self.__hovered_cell = cell
            else:
                self.__hovered_cell = None
        else:
            self.__hovered_cell = None
