from typing import Tuple

import pygame

from model.map.grid import Grid
from model.simulation.mas_stats import MASEvolutionStats

from .config import SIDEBAR_WIDTH
from .renderers.agent import AgentRenderer
from .renderers.grid import GridRenderer
from .renderers.sidebar import SidebarRenderer


class Renderer:
    def __init__(self, screen: pygame.Surface, grid: Grid, cell_size: int) -> None:
        self._screen = screen

        grid_width_px = grid._width * cell_size
        grid_height_px = grid._height * cell_size

        grid_area_width = screen.get_width() - SIDEBAR_WIDTH
        offset_x = (grid_area_width - grid_width_px) // 2
        offset_y = (screen.get_height() - grid_height_px) // 2

        self.__grid_r = GridRenderer(screen, grid, cell_size, offset_x, offset_y)
        self.__agent_r = AgentRenderer(screen, grid, cell_size, offset_x, offset_y)
        self.__sidebar_r = SidebarRenderer(screen, grid, grid_area_width)

    def render(
        self,
        hovered_cell: Tuple[int, int] | None,
        selected_cell: Tuple[int, int] | None,
        epoch: int,
        total_agents: int,
        speed_label: str,
        mas_stats: MASEvolutionStats | None = None,
    ) -> None:
        self.__grid_r.render_background()
        self.__grid_r.render_lines()
        self.__grid_r.render_barriers()
        self.__agent_r.render_all()
        self.__sidebar_r.render(
            hovered_cell, selected_cell, epoch, total_agents, speed_label, mas_stats
        )

    def is_in_grid_area(self, screen_x: int, screen_y: int) -> bool:
        return self.__grid_r.contains(screen_x, screen_y)

    def screen_to_grid(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        return self.__grid_r.to_grid(screen_x, screen_y)

    def count_agents(self) -> int:
        return sum(
            len(r.agents) for r in self.__grid_r.grid.regions if not r.is_barrier
        )
