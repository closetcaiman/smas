"""
Grid renderer.
"""

import pygame

from model.map.grid import Grid
from model.map.region import Region

from .. import config


class GridRenderer:
    """Renders grid background and barriers."""

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
        self.__grid_width_px = grid._width * cell_size
        self.__grid_height_px = grid._height * cell_size

    @property
    def grid(self) -> Grid:
        return self.__grid

    def render_background(self) -> None:
        for i in range(self.__grid._height):
            for j in range(self.__grid._width):
                pygame.draw.rect(
                    self.__screen,
                    self.__grid.color_at(j, i),
                    pygame.Rect(
                        self.__offset_x + j * self.__cell_size,
                        self.__offset_y + i * self.__cell_size,
                        self.__cell_size,
                        self.__cell_size,
                    ),
                )

    def render_lines(self) -> None:
        for i in range(self.__grid._height + 1):
            y = self.__offset_y + i * self.__cell_size
            pygame.draw.line(
                self.__screen,
                config.GRID_LINE_COLOR,
                (self.__offset_x, y),
                (self.__offset_x + self.__grid_width_px, y),
            )
        for j in range(self.__grid._width + 1):
            x = self.__offset_x + j * self.__cell_size
            pygame.draw.line(
                self.__screen,
                config.GRID_LINE_COLOR,
                (x, self.__offset_y),
                (x, self.__offset_y + self.__grid_height_px),
            )

    def render_barriers(self) -> None:
        for row in self.__grid._data:
            for region in row:
                if region.is_barrier:
                    self.__render_barrier(region)

    def __render_barrier(self, region: Region) -> None:
        coords = self.__get_coords(region)
        if coords is None:
            return
        x, y = coords
        rect = pygame.Rect(
            self.__offset_x + x * self.__cell_size + 1,
            self.__offset_y + y * self.__cell_size + 1,
            self.__cell_size - 2,
            self.__cell_size - 2,
        )
        pygame.draw.rect(self.__screen, config.BARRIER_COLOR, rect)

    def __get_coords(self, region: Region) -> tuple | None:
        for y, row in enumerate(self.__grid._data):
            for x, r in enumerate(row):
                if r is region:
                    return (x, y)
        return None

    def contains(self, screen_x: int, screen_y: int) -> bool:
        return (
            self.__offset_x <= screen_x < self.__offset_x + self.__grid_width_px
            and self.__offset_y <= screen_y < self.__offset_y + self.__grid_height_px
        )

    def to_grid(self, screen_x: int, screen_y: int) -> tuple:
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
        if 0 <= cell_x < self.__grid._width and 0 <= cell_y < self.__grid._height:
            return (cell_x, cell_y)
        return (-1, -1)
