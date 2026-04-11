"""
Agent renderer.
"""

import pygame

from model.map.grid import Grid
from model.map.region import Region

from .. import config


class AgentRenderer:
    """Renders agents."""

    def __init__(
        self,
        screen: pygame.Surface,
        grid: Grid,
        cell_size: int,
        offset_x: int,
        offset_y: int,
    ) -> None:
        self.__screen = screen
        self.__grid = grid
        self.__cell_size = cell_size
        self.__offset_x = offset_x
        self.__offset_y = offset_y

    def render_all(self) -> None:
        for row in self.__grid._data:
            for region in row:
                if region.agents and not region.is_barrier:
                    self.__render_agent(region)

    def __render_agent(self, region: Region) -> None:
        coords = self.__get_coords(region)
        if coords is None:
            return
        cell_x, cell_y = coords
        center_x = self.__offset_x + cell_x * self.__cell_size + self.__cell_size // 2
        center_y = self.__offset_y + cell_y * self.__cell_size + self.__cell_size // 2

        agents = region.agents
        avg_size = sum(a.genome.size.value for a in agents) / len(agents)
        avg_metabolic = sum(a.genome.metabolic_rate.value for a in agents) / len(agents)
        avg_ideal_temp = sum(a.genome.ideal_temperature.value for a in agents) / len(
            agents
        )
        avg_temp_tol = sum(a.genome.temperature_tolerance.value for a in agents) / len(
            agents
        )

        radius = self.__radius_from_size(avg_size)
        color = self.__color_from_genome(avg_metabolic, avg_ideal_temp, avg_temp_tol)

        pygame.draw.circle(self.__screen, color, (center_x, center_y), radius)
        pygame.draw.circle(
            self.__screen,
            config.AGENT_OUTLINE_COLOR,
            (center_x, center_y),
            radius,
            config.AGENT_OUTLINE_WIDTH,
        )

    def __radius_from_size(self, size: float) -> int:
        normalized = (size - config.AGENT_SIZE_MIN) / (
            config.AGENT_SIZE_MAX - config.AGENT_SIZE_MIN
        )
        return int(
            config.AGENT_BASE_RADIUS
            * (
                config.RADIUS_FACTOR_MIN
                + normalized * (config.RADIUS_FACTOR_MAX - config.RADIUS_FACTOR_MIN)
            )
        )

    def __color_from_genome(
        self, metabolic: float, ideal_temp: float, temp_tol: float
    ) -> tuple:
        r = int(
            80
            + (metabolic - config.METABOLIC_RANGE_MIN)
            / (config.METABOLIC_RANGE_MAX - config.METABOLIC_RANGE_MIN)
            * 175
        )
        g = int(
            80
            + (ideal_temp - config.IDEAL_TEMP_RANGE_MIN)
            / (config.IDEAL_TEMP_RANGE_MAX - config.IDEAL_TEMP_RANGE_MIN)
            * 175
        )
        b = int(
            80
            + (temp_tol - config.TEMP_TOL_RANGE_MIN)
            / (config.TEMP_TOL_RANGE_MAX - config.TEMP_TOL_RANGE_MIN)
            * 175
        )
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    def __get_coords(self, region: Region) -> tuple | None:
        for y, row in enumerate(self.__grid._data):
            for x, r in enumerate(row):
                if r is region:
                    return (x, y)
        return None
