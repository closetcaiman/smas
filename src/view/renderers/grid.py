import pygame

from config.default import ViewConfig
from controller.handlers.sampling import WorldMapSample
from model.world import World
from view.renderers.ui_renderer import UIRenderer
from view.types import RenderContext
from view.viewport import Viewport


class GridRenderer(UIRenderer):
    """Renders grid background and barriers."""

    def __init__(
        self,
        viewport: Viewport,
        world: World,
        sample: WorldMapSample,
        config: ViewConfig,
    ) -> None:
        """
        Initialize the grid renderer.

        Args:
            viewport: The viewport to use for rendering.
            world: The world to render.
            sample: The world map sample.
            cell_size: The size of each grid cell.
            offset_x: The x-coordinate offset for rendering the grid.
            offset_y: The y-coordinate offset for rendering the grid.
            config: The view configuration containing settings for rendering.

        """
        self.__config = config
        self.__screen = viewport.screen
        self.__world = world
        self.__world_sample = sample
        self.__cell_size = viewport.cell_size
        self.__offset_x = viewport.offset[0] + config.METRICS_PANEL_WIDTH
        self.__offset_y = viewport.offset[1]
        self.__grid_width_px = world.width * self.__cell_size
        self.__grid_height_px = world.height * self.__cell_size

    def render(self, context: RenderContext) -> None:
        """
        Render the grid background and barriers.

        Overrides:
            UIRenderer.render: Draws the grid background based on the world sample data, renders the grid lines,
                and then renders barriers on the grid based on the world state.
        """
        self.__render_background()
        self.__render_lines()
        self.__render_barriers()

    def contains(self, screen_x: int, screen_y: int) -> bool:
        """
        Check if the given screen coordinates are within the grid area.

        Args:
            screen_x: The x-coordinate on the screen.
            screen_y: The y-coordinate on the screen.

        Returns:
            True if the coordinates are within the grid area, False otherwise.

        """
        return (
            self.__offset_x <= screen_x < self.__offset_x + self.__grid_width_px
            and self.__offset_y <= screen_y < self.__offset_y + self.__grid_height_px
        )

    def to_grid(self, screen_x: int, screen_y: int) -> tuple:
        """
        Convert screen coordinates to grid coordinates.

        Args:
            screen_x: The x-coordinate on the screen.
            screen_y: The y-coordinate on the screen.

        Returns:
            A tuple containing the grid coordinates (x, y) if the screen coordinates are within the grid area, (-1, -1) otherwise.

        """
        if (
            screen_x < self.__offset_x
            or screen_x >= self.__offset_x + self.__grid_width_px
        ):
            return (-1, -1)
        if (
            screen_y < self.__offset_y
            or screen_y >= self.__offset_y + self.__grid_height_px
        ):
            return (-1, -1)
        cell_x = (screen_x - self.__offset_x) // self.__cell_size
        cell_y = (screen_y - self.__offset_y) // self.__cell_size
        if 0 <= cell_x < self.__world.width and 0 <= cell_y < self.__world.height:
            return (cell_x, cell_y)
        return (-1, -1)

    def __render_background(self) -> None:
        """Render the grid background based on the world sample data."""
        for i in range(self.__world.height):
            for j in range(self.__world.width):
                pygame.draw.rect(
                    self.__screen,
                    self.__world_sample.color_at(j, i),
                    pygame.Rect(
                        self.__offset_x + j * self.__cell_size,
                        self.__offset_y + i * self.__cell_size,
                        self.__cell_size,
                        self.__cell_size,
                    ),
                )

    def __render_lines(self) -> None:
        """Render the grid lines."""
        for i in range(self.__world.height + 1):
            y = self.__offset_y + i * self.__cell_size
            pygame.draw.line(
                self.__screen,
                self.__config.GRID_LINE_COLOR,
                (self.__offset_x, y),
                (self.__offset_x + self.__grid_width_px, y),
            )
        for j in range(self.__world.width + 1):
            x = self.__offset_x + j * self.__cell_size
            pygame.draw.line(
                self.__screen,
                self.__config.GRID_LINE_COLOR,
                (x, self.__offset_y),
                (x, self.__offset_y + self.__grid_height_px),
            )

    def __render_barriers(self) -> None:
        """Render barriers on the grid."""
        for region in self.__world.regions:
            if region.is_barrier:
                x, y = region.coordinates
                rect = pygame.Rect(
                    self.__offset_x + x * self.__cell_size + 1,
                    self.__offset_y + y * self.__cell_size + 1,
                    self.__cell_size - 2,
                    self.__cell_size - 2,
                )
                pygame.draw.rect(self.__screen, self.__config.BARRIER_COLOR, rect)
