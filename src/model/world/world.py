from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, List

from model.world.elements.food import FoodResources
from model.world.elements.region import Region
from model.world.types import PopulationType

if TYPE_CHECKING:
    from controller.handlers import WorldMapSample


class World:
    """
    Represents the entire simulation environment, including the grid of regions and their interactions.

    Attributes:
        regions: Iterator[Region] - An iterator over all regions in the world.
        width: int - The width of the world grid.
        height: int - The height of the world grid.

    """

    __regions: List[List[Region]]
    __width: int
    __height: int

    def __init__(self, width: int, height: int, sample: WorldMapSample) -> None:
        """Initialize the world with the given dimensions and sample data."""
        self.__regions = [[] for _ in range(height)]
        self.__width = width
        self.__height = height
        self.__sample = sample

        for i in range(self.__height):
            for j in range(self.__width):
                grass_seed = self.__sample.grass_seed(i, j)
                tall_grass_seed = self.__sample.tall_grass_seed(i, j)
                fruit_seed = self.__sample.fruit_seed(i, j)
                migration_cost_seed = self.__sample.migration_cost_seed(i, j)
                population_type = (
                    PopulationType.A if i < self.__width // 2 else PopulationType.B
                )
                self.__regions[i].append(
                    Region(
                        food=FoodResources(
                            grass_amount=grass_seed["grass_amount"],
                            grass_growth=grass_seed["grass_growth"],
                            grass_max_amount=grass_seed["grass_max_amount"],
                            tall_grass_amount=tall_grass_seed["tall_grass_amount"],
                            tall_grass_growth=tall_grass_seed["tall_grass_growth"],
                            tall_grass_max_amount=tall_grass_seed[
                                "tall_grass_max_amount"
                            ],
                            fruit_amount=fruit_seed["fruit_amount"],
                            fruit_growth=fruit_seed["fruit_growth"],
                            fruit_max_amount=fruit_seed["fruit_max_amount"],
                        ),
                        migrate_in_cost=migration_cost_seed["migrate_in_cost"],
                        migrate_out_cost=migration_cost_seed["migrate_out_cost"],
                        max_agents=self.__sample.max_agents_seed(i, j),
                        temperature=self.__sample.temperature_seed(i, j),
                        neighbors=[],
                        coordinates=(i, j),
                        agents=[],
                        population_type=population_type,
                    )
                )

        for i in range(self.__height):
            for j in range(self.__width):
                if i > 0:
                    self.__regions[i][j].neighbors.append(self.__regions[i - 1][j])
                if i + 1 < self.__height:
                    self.__regions[i][j].neighbors.append(self.__regions[i + 1][j])
                if j > 0:
                    self.__regions[i][j].neighbors.append(self.__regions[i][j - 1])
                if j + 1 < self.__width:
                    self.__regions[i][j].neighbors.append(self.__regions[i][j + 1])

    @property
    def regions(self) -> Iterator[Region]:
        """Iterator over all regions in the world."""
        for row in self.__regions:
            for region in row:
                yield region

    @property
    def grid_width(self) -> int:
        """Width of the world grid."""
        return self.__width

    @property
    def grid_height(self) -> int:
        """Height of the world grid."""
        return self.__height

    def region_at(self, x: int, y: int) -> Region:
        """Get the region at the specified coordinates."""
        if 0 <= y < self.__height and 0 <= x < self.__width:
            return self.__regions[y][x]

        raise IndexError(
            f"Coordinates ({x}, {y}) are out of bounds for world of size {self.__width}x{self.__height}"
        )

    @property
    def width(self) -> int:
        """Width of the world grid."""
        return self.__width

    @property
    def height(self) -> int:
        """Height of the world grid."""
        return self.__height
