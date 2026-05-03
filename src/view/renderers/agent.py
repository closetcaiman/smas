import pygame

from config.default import ViewConfig
from model.world import Region, World
from view.renderers.ui_renderer import UIRenderer
from view.types import RenderContext
from view.viewport import Viewport


class AgentRenderer(UIRenderer):
    """Renders agents."""

    def __init__(
        self,
        viewport: Viewport,
        world: World,
        config: ViewConfig,
    ) -> None:
        """
        Initialize the agent renderer.

        Args:
            viewport: The viewport for rendering.
            world: The world to render.
            cell_size: The size of each grid cell.
            offset_x: The x-coordinate offset for rendering the grid.
            offset_y: The y-coordinate offset for rendering the grid.
            config: The view configuration containing settings for rendering.

        """
        self.__screen = viewport.screen
        self.__config = config
        self.__world = world
        self.__cell_size = viewport.cell_size
        self.__offset_x = viewport.offset[0]
        self.__offset_y = viewport.offset[1]

    def render(self, context: RenderContext) -> None:
        """
        Render all agents on the grid.

        Overrides:
            UIRenderer.render: Iterates through all regions in the world and renders an agent for
                each region that contains agents and is not a barrier. The agent's appearance is determined by the
        """
        for region in self.__world.regions:
            if region.agents and not region.is_barrier:
                self.__render_agent(region)

    def __render_agent(self, region: Region) -> None:
        cell_x, cell_y = region.coordinates
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
            self.__config.AGENT_OUTLINE_COLOR,
            (center_x, center_y),
            radius,
            self.__config.AGENT_OUTLINE_WIDTH,
        )

    def __radius_from_size(self, size: float) -> int:
        normalized = (size - self.__config.AGENT_SIZE_MIN) / (
            self.__config.AGENT_SIZE_MAX - self.__config.AGENT_SIZE_MIN
        )
        return int(
            self.__config.AGENT_BASE_RADIUS
            * (
                self.__config.RADIUS_FACTOR_MIN
                + normalized
                * (self.__config.RADIUS_FACTOR_MAX - self.__config.RADIUS_FACTOR_MIN)
            )
        )

    def __color_from_genome(
        self, metabolic: float, ideal_temp: float, temp_tol: float
    ) -> tuple:
        r = int(
            80
            + (metabolic - self.__config.METABOLIC_RANGE_MIN)
            / (self.__config.METABOLIC_RANGE_MAX - self.__config.METABOLIC_RANGE_MIN)
            * 175
        )
        g = int(
            80
            + (ideal_temp - self.__config.IDEAL_TEMP_RANGE_MIN)
            / (self.__config.IDEAL_TEMP_RANGE_MAX - self.__config.IDEAL_TEMP_RANGE_MIN)
            * 175
        )
        b = int(
            80
            + (temp_tol - self.__config.TEMP_TOL_RANGE_MIN)
            / (self.__config.TEMP_TOL_RANGE_MAX - self.__config.TEMP_TOL_RANGE_MIN)
            * 175
        )
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
