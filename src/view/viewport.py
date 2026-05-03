from dataclasses import dataclass
from typing import Tuple

import pygame


@dataclass
class Viewport:
    """Manages the viewport for rendering the grid and sidebar."""

    screen: pygame.Surface
    grid_width: int
    grid_height: int
    sidebar_width: int
    offset_x: int

    def __init__(
        self,
        screen: pygame.Surface,
        grid_width: int,
        grid_height: int,
        sidebar_width: int,
        offset_x: int,
    ) -> None:
        """
        Initialize the viewport with the given parameters.

        Args:
            screen: The pygame surface to render on.
            grid_width: The width of the grid in cells.
            grid_height: The height of the grid in cells.
            sidebar_width: The width of the sidebar in pixels.
            offset_x: The x-coordinate offset for rendering the grid (to account for metrics panel).

        """
        self.screen = screen
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.sidebar_width = sidebar_width
        self.offset_x = offset_x

        # Must be initialized in this order:
        # grid_area_width -> cell_size -> offset | sidebar_x

        self.grid_area_width = self.__calculate_grid_area_width()
        self.cell_size = self.__calculate_cell_size()
        self.offset = self.__calculate_offset()
        self.sidebar_x = self.__calculate_sidebar_x()

    def is_in_grid_area(self, x: int, y: int) -> bool:
        """
        Check if the given screen coordinates are within the grid area.

        Args:
            x: The x-coordinate on the screen.
            y: The y-coordinate on the screen.

        Returns:
            True if the coordinates are within the grid area, False otherwise.

        """
        off_x, off_y = self.offset
        return off_x <= x < off_x + (
            self.grid_width * self.cell_size
        ) and off_y <= y < off_y + (self.grid_height * self.cell_size)

    def screen_to_grid(self, x: int, y: int) -> Tuple[int, int]:
        """
        Convert screen coordinates to grid coordinates.

        Args:
            x: The x-coordinate on the screen.
            y: The y-coordinate on the screen.

        Returns:
            A tuple containing the grid coordinates (x, y) if the screen coordinates are within the grid area, (-1, -1) otherwise.

        """
        off_x, off_y = self.offset
        grid_x = (x - off_x) // self.cell_size
        grid_y = (y - off_y) // self.cell_size
        return int(grid_x), int(grid_y)

    def __calculate_grid_area_width(self) -> int:
        """Calculate the width of the area available for rendering the grid."""
        return self.screen.get_width() - self.sidebar_width

    def __calculate_sidebar_x(self) -> int:
        """Calculate the x-coordinate where the sidebar starts."""
        return self.grid_area_width

    def __calculate_cell_size(self) -> int:
        """Calculate the size of each grid cell based on the available area."""
        grid_area_width = self.screen.get_width() - self.sidebar_width
        grid_area_height = self.screen.get_height()
        return min(
            grid_area_width // self.grid_width,
            grid_area_height // self.grid_height,
        )

    def __calculate_offset(self) -> Tuple[int, int]:
        """Calculate the pixel offset to center the grid within the available area."""
        grid_w_px = self.grid_width * self.cell_size
        grid_h_px = self.grid_height * self.cell_size
        off_x = (self.grid_area_width - grid_w_px) // 2
        off_y = (self.screen.get_height() - grid_h_px) // 2
        return off_x, off_y
