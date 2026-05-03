from typing import Tuple

import pygame

from config.default import ViewConfig
from model.world import Region, World
from view.types import RenderContext
from view.viewport import Viewport


class SidebarRenderer:
    """Renders the sidebar with simulation information and controls."""

    def __init__(self, viewport: Viewport, world: World, config: ViewConfig) -> None:
        """
        Initialize the sidebar renderer.

        Args:
            viewport: The viewport to use for rendering.
            world: The world to render information about.
            config: The view configuration.

        Returns:
            None

        """
        self.__config = config
        self.__screen = viewport.screen
        self.__world = world
        self.__sidebar_x = viewport.sidebar_x + config.METRICS_PANEL_WIDTH
        self.__title_font = pygame.font.Font(None, self.__config.TITLE_FONT_SIZE)
        self.__hud_font = pygame.font.Font(None, self.__config.HUD_FONT_SIZE)
        self.__small_font = pygame.font.Font(None, self.__config.SMALL_FONT_SIZE)

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
            self.__screen,
            self.__config.SIDEBAR_BG_COLOR,
            (
                self.__sidebar_x,
                0,
                self.__config.SIDEBAR_WIDTH,
                self.__screen.get_height(),
            ),
        )
        pygame.draw.line(
            self.__screen,
            self.__config.SIDEBAR_BORDER_COLOR,
            (self.__sidebar_x, 0),
            (self.__sidebar_x, self.__screen.get_height()),
            self.__config.SIDEBAR_BORDER_WIDTH,
        )

    def __render_header(self, epoch: int, total_agents: int, speed_label: str) -> None:
        x = self.__sidebar_x + self.__config.SIDEBAR_MARGIN
        y = self.__config.SIDEBAR_MARGIN
        self.__screen.blit(
            self.__title_font.render("MAS Simulation", True, self.__config.TEXT_COLOR),
            (x, y),
        )
        y += 45
        self.__screen.blit(
            self.__hud_font.render(f"Epoch: {epoch}", True, self.__config.TEXT_COLOR),
            (x, y),
        )
        y += 30
        self.__screen.blit(
            self.__hud_font.render(
                f"Alive: {total_agents}", True, self.__config.HEALTH_COLOR
            ),
            (x, y),
        )
        y += 30
        self.__screen.blit(
            self.__hud_font.render(
                f"Speed: {speed_label}", True, self.__config.WARNING_COLOR
            ),
            (x, y),
        )

    def __render_controls(self) -> None:
        x = self.__sidebar_x + self.__config.SIDEBAR_MARGIN
        y = self.__screen.get_height() - 200
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
            self.__screen.blit(
                self.__small_font.render(line, True, self.__config.LABEL_COLOR), (x, y)
            )
            y += 20

    def __render_hovered(self, cell: Tuple[int, int]) -> None:
        x, y = cell
        region = self.__world.region_at(y, x)
        self.__render_cell_info(x, y, region, 240)

    def __render_selected(self, cell: Tuple[int, int]) -> None:
        x, y = cell
        region = self.__world.region_at(y, x)
        pos_x = self.__sidebar_x + self.__config.SIDEBAR_MARGIN
        pos_y = 240
        self.__screen.blit(
            self.__hud_font.render(f"Cell ({x}, {y})", True, self.__config.TEXT_COLOR),
            (pos_x, pos_y),
        )
        pos_y += 35
        pygame.draw.rect(
            self.__screen,
            self.__config.BARRIER_COLOR
            if region.is_barrier
            else self.__config.ENLARGED_BG_COLOR,
            (pos_x, pos_y, self.__config.ENLARGED_SIZE, self.__config.ENLARGED_SIZE),
        )
        if region.agents and not region.is_barrier:
            self.__render_enlarged_agents(region, pos_x, pos_y)
        pos_y += self.__config.ENLARGED_SIZE + 25
        self.__render_region_stats(region, pos_x, pos_y)

    def __render_enlarged_agents(self, region: Region, x: int, y: int) -> None:
        if not region.agents:
            return
        center_x = x + self.__config.ENLARGED_SIZE // 2
        center_y = y + self.__config.ENLARGED_SIZE // 2
        spacing = self.__config.ENLARGED_AGENT_SPACING
        num_show = min(len(region.agents), self.__config.ENLARGED_MAX_DISPLAY)
        start_offset = -(num_show - 1) * spacing // 2

        for i in range(num_show):
            agent = region.agents[i]
            size = agent.genome.size.value
            normalized = (size - self.__config.AGENT_SIZE_MIN) / (
                self.__config.AGENT_SIZE_MAX - self.__config.AGENT_SIZE_MIN
            )
            radius = max(
                self.__config.ENLARGED_MIN_RADIUS,
                int(
                    self.__config.AGENT_BASE_RADIUS
                    * (
                        self.__config.RADIUS_FACTOR_MIN
                        + normalized
                        * (
                            self.__config.RADIUS_FACTOR_MAX
                            - self.__config.RADIUS_FACTOR_MIN
                        )
                    )
                    * self.__config.ENLARGED_AGENT_SCALE
                ),
            )

            metabolic = agent.genome.metabolic_rate.value
            ideal_temp = agent.genome.ideal_temperature.value
            temp_tol = agent.genome.temperature_tolerance.value
            r = int(
                80
                + (metabolic - self.__config.METABOLIC_RANGE_MIN)
                / (
                    self.__config.METABOLIC_RANGE_MAX
                    - self.__config.METABOLIC_RANGE_MIN
                )
                * 175
            )
            g = int(
                80
                + (ideal_temp - self.__config.IDEAL_TEMP_RANGE_MIN)
                / (
                    self.__config.IDEAL_TEMP_RANGE_MAX
                    - self.__config.IDEAL_TEMP_RANGE_MIN
                )
                * 175
            )
            b = int(
                80
                + (temp_tol - self.__config.TEMP_TOL_RANGE_MIN)
                / (self.__config.TEMP_TOL_RANGE_MAX - self.__config.TEMP_TOL_RANGE_MIN)
                * 175
            )
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

            offset_x = center_x + start_offset + i * spacing
            pygame.draw.circle(self.__screen, color, (offset_x, center_y), radius)
            pygame.draw.circle(
                self.__screen,
                self.__config.AGENT_OUTLINE_COLOR,
                (offset_x, center_y),
                radius,
                self.__config.AGENT_OUTLINE_WIDTH,
            )

    def __render_cell_info(
        self, cell_x: int, cell_y: int, region: Region, start_y: int
    ) -> None:
        self.__screen.blit(
            self.__hud_font.render(
                f"Cell ({cell_x}, {cell_y})", True, self.__config.TEXT_COLOR
            ),
            (self.__sidebar_x + self.__config.SIDEBAR_MARGIN, start_y),
        )
        start_y += 32
        self.__render_region_stats(
            region, self.__sidebar_x + self.__config.SIDEBAR_MARGIN, start_y
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
            self.__screen.blit(
                self.__small_font.render(line, True, self.__config.LABEL_COLOR), (x, y)
            )
            y += 18
        if region.agents:
            y += 10
            self.__screen.blit(
                self.__small_font.render("Agents:", True, self.__config.TEXT_COLOR),
                (x, y),
            )
            y += 18
            for i, agent in enumerate(region.agents[:4]):
                self.__screen.blit(
                    self.__small_font.render(
                        f"#{i + 1}: E={agent.energy} A={agent.age}",
                        True,
                        self.__config.LABEL_COLOR,
                    ),
                    (x, y),
                )
                y += 16
