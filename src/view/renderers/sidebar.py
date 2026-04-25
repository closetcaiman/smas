from typing import Tuple

import pygame

from model.world import Region, World
from view.types import RenderContext
from view.viewport import Viewport

from .. import config


class SidebarRenderer:
    """Renders the sidebar with simulation information and controls."""

    def __init__(self, viewport: Viewport, world: World) -> None:
        """
        Initialize the sidebar renderer.

        Args:
            viewport: The viewport to use for rendering.
            world: The world to render information about.

        Returns:
            None

        """
        self._screen = viewport.screen
        self._world = world
        self._sidebar_x = viewport.sidebar_x
        self._title_font = pygame.font.Font(None, config.TITLE_FONT_SIZE)
        self._hud_font = pygame.font.Font(None, config.HUD_FONT_SIZE)
        self._small_font = pygame.font.Font(None, config.SMALL_FONT_SIZE)

    def render(
        self,
        context: RenderContext,
    ) -> None:
        """
        Render the sidebar with current simulation information and controls.

        Overrides:
            UIRenderer.render: Draws the sidebar background, header information (epoch, total agents, speed), and controls.
            If a cell is selected or hovered, it also renders detailed information about that cell and its region.
        """
        self.__render_background()
        self.__render_header(context.epoch, context.total_agents, context.speed_label)

        if context.selected_cell:
            self.__render_selected(context.selected_cell)
        elif context.hovered_cell:
            self.__render_hovered(context.hovered_cell)

        self.__render_controls()

    def __render_background(self) -> None:
        pygame.draw.rect(
            self._screen,
            config.SIDEBAR_BG_COLOR,
            (self._sidebar_x, 0, config.SIDEBAR_WIDTH, self._screen.get_height()),
        )
        pygame.draw.line(
            self._screen,
            config.SIDEBAR_BORDER_COLOR,
            (self._sidebar_x, 0),
            (self._sidebar_x, self._screen.get_height()),
            config.SIDEBAR_BORDER_WIDTH,
        )

    def __render_header(self, epoch: int, total_agents: int, speed_label: str) -> None:
        x = self._sidebar_x + config.SIDEBAR_MARGIN
        y = config.SIDEBAR_MARGIN
        self._screen.blit(
            self._title_font.render("MAS Simulation", True, config.TEXT_COLOR), (x, y)
        )
        y += 45
        self._screen.blit(
            self._hud_font.render(f"Epoch: {epoch}", True, config.TEXT_COLOR), (x, y)
        )
        y += 30
        self._screen.blit(
            self._hud_font.render(f"Alive: {total_agents}", True, config.HEALTH_COLOR),
            (x, y),
        )
        y += 30
        self._screen.blit(
            self._hud_font.render(f"Speed: {speed_label}", True, config.WARNING_COLOR),
            (x, y),
        )

    def __render_controls(self) -> None:
        x = self._sidebar_x + config.SIDEBAR_MARGIN
        y = self._screen.get_height() - 200
        for line in (
            "Controls:",
            "  ESC/Q - Quit",
            "  Up/Down - Speed",
            "  B - Barrier",
            "  Space - Pause",
            "  R - Reset",
            "  S - Save Data",
            "  Click - Select",
        ):
            self._screen.blit(
                self._small_font.render(line, True, config.LABEL_COLOR), (x, y)
            )
            y += 20

    def __render_hovered(self, cell: Tuple[int, int]) -> None:
        x, y = cell
        region = self._world.region_at(x, y)
        self.__render_cell_info(x, y, region, 240)

    def __render_selected(self, cell: Tuple[int, int]) -> None:
        x, y = cell
        region = self._world.region_at(x, y)
        pos_x = self._sidebar_x + config.SIDEBAR_MARGIN
        pos_y = 240
        self._screen.blit(
            self._hud_font.render(f"Cell ({x}, {y})", True, config.TEXT_COLOR),
            (pos_x, pos_y),
        )
        pos_y += 35
        pygame.draw.rect(
            self._screen,
            config.BARRIER_COLOR if region.is_barrier else config.ENLARGED_BG_COLOR,
            (pos_x, pos_y, config.ENLARGED_SIZE, config.ENLARGED_SIZE),
        )
        if region.agents and not region.is_barrier:
            self.__render_enlarged_agents(region, pos_x, pos_y)
        pos_y += config.ENLARGED_SIZE + 25
        self.__render_region_stats(region, pos_x, pos_y)

    def __render_enlarged_agents(self, region: Region, x: int, y: int) -> None:
        if not region.agents:
            return
        center_x = x + config.ENLARGED_SIZE // 2
        center_y = y + config.ENLARGED_SIZE // 2
        spacing = config.ENLARGED_AGENT_SPACING
        num_show = min(len(region.agents), config.ENLARGED_MAX_DISPLAY)
        start_offset = -(num_show - 1) * spacing // 2

        for i in range(num_show):
            agent = region.agents[i]
            size = agent.genome.size.value
            normalized = (size - config.AGENT_SIZE_MIN) / (
                config.AGENT_SIZE_MAX - config.AGENT_SIZE_MIN
            )
            radius = max(
                config.ENLARGED_MIN_RADIUS,
                int(
                    config.AGENT_BASE_RADIUS
                    * (
                        config.RADIUS_FACTOR_MIN
                        + normalized
                        * (config.RADIUS_FACTOR_MAX - config.RADIUS_FACTOR_MIN)
                    )
                    * config.ENLARGED_AGENT_SCALE
                ),
            )

            metabolic = agent.genome.metabolic_rate.value
            ideal_temp = agent.genome.ideal_temperature.value
            temp_tol = agent.genome.temperature_tolerance.value
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
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

            offset_x = center_x + start_offset + i * spacing
            pygame.draw.circle(self._screen, color, (offset_x, center_y), radius)
            pygame.draw.circle(
                self._screen,
                config.AGENT_OUTLINE_COLOR,
                (offset_x, center_y),
                radius,
                config.AGENT_OUTLINE_WIDTH,
            )

    def __render_cell_info(
        self, cell_x: int, cell_y: int, region: Region, start_y: int
    ) -> None:
        self._screen.blit(
            self._hud_font.render(
                f"Cell ({cell_x}, {cell_y})", True, config.TEXT_COLOR
            ),
            (self._sidebar_x + config.SIDEBAR_MARGIN, start_y),
        )
        start_y += 32
        self.__render_region_stats(
            region, self._sidebar_x + config.SIDEBAR_MARGIN, start_y
        )

    def __render_region_stats(self, region: Region, x: int, y: int) -> None:
        lines = (
            f"Barrier: {region.is_barrier}",
            f"Temperature: {region.temperature}",
            f"Agents: {len(region.agents)}",
            f"Max: {region.max_agents}",
            f"In: {region.migrate_in_cost} Out: {region.migrate_out_cost}",
        )
        for line in lines:
            self._screen.blit(
                self._small_font.render(line, True, config.LABEL_COLOR), (x, y)
            )
            y += 18
        if region.agents:
            y += 10
            self._screen.blit(
                self._small_font.render("Agents:", True, config.TEXT_COLOR), (x, y)
            )
            y += 18
            for i, agent in enumerate(region.agents[:4]):
                self._screen.blit(
                    self._small_font.render(
                        f"#{i + 1}: E={agent.energy} A={agent.age}",
                        True,
                        config.LABEL_COLOR,
                    ),
                    (x, y),
                )
                y += 16
