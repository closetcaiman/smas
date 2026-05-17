from colorsys import hsv_to_rgb
from dataclasses import dataclass

import numpy as np

from controller.types import FruitSeed, GrassSeed, MigrationCostSeed, TallGrassSeed


@dataclass
class WorldMapSample:
    """
    Data class to hold the sampled HSV data for the world map.

    This class provides methods to derive various properties of the world based
    on the HSV values at each cell, such as vegetation growth, migration costs, and temperature.

    Attributes:
        hsv_data: A 3D numpy array of shape (height, width, 3) containing the average HSV values for each cell in the grid.

    Methods:
        grass_seed(x: int, y: int) -> GrassSeed: Derive grass growth properties based on the HSV values at the given cell coordinates.
        tall_grass_seed(x: int, y: int) -> TallGrassSeed: Derive tall grass growth properties based on the HSV values at the given cell coordinates.
        fruit_seed(x: int, y: int) -> FruitSeed: Derive fruit growth properties based on the HSV values at the given cell coordinates.
        migration_cost_seed(x: int, y: int) -> MigrationCostSeed: Derive migration cost properties based on the HSV values at the given cell coordinates.
        max_agents_seed(x: int, y: int) -> int: Derive the maximum number of agents that can be supported in the cell based on the HSV values at the given cell coordinates.
        temperature_seed(x: int, y: int) -> int: Derive the temperature of the cell based on the HSV values at the given cell coordinates.
        color_at(x: int, y: int) -> list[int]: Get the RGB color corresponding to the HSV values at the given cell coordinates for rendering purposes.

    """

    hsv_data: np.ndarray

    def grass_seed(self, x: int, y: int) -> GrassSeed:
        """Grass grows best in areas with moderate saturation (some resources) and sufficient light."""
        green_index = abs(
            self.__hue(x, y) - 120
        )  # 120 - angle for green, green_index == 0 -> greenest
        vegetation_factor = max(0, 100 - abs(self.__hue(x, y) - 120)) / 100
        light_factor = max(0, self.__value(x, y) - 155) / 100
        return {
            "grass_amount": int(20 * vegetation_factor),
            "grass_growth": int(10 * light_factor),
            "grass_max_amount": int(50 * vegetation_factor),
        }

    def tall_grass_seed(self, x: int, y: int) -> TallGrassSeed:
        """Only grows in areas with some saturation (enough resources) and sufficient light."""
        saturation_factor = self.__saturation(x, y) / 255
        has_tall_grass = saturation_factor > 0.3
        vegetation_factor = max(0, 100 - abs(self.__hue(x, y) - 120)) / 100
        light_factor = max(0, self.__value(x, y) - 155) / 100
        return {
            "tall_grass_amount": int(10 * vegetation_factor) if has_tall_grass else 0,
            "tall_grass_growth": int(10 * light_factor) if has_tall_grass else 0,
            "tall_grass_max_amount": int(30 * vegetation_factor)
            if has_tall_grass
            else 0,
        }

    def fruit_seed(self, x: int, y: int) -> FruitSeed:
        """Fruiting plants only grow in areas with high saturation (more resources) and sufficient light."""
        saturation_factor = self.__saturation(x, y) / 255
        has_fruit = saturation_factor > 0.5
        vegetation_factor = max(0, 100 - abs(self.__hue(x, y) - 120)) / 100
        light_factor = max(0, self.__value(x, y) - 155) / 100
        return {
            "fruit_amount": int(10 * vegetation_factor) if has_fruit else 0,
            "fruit_growth": int(10 * light_factor) if has_fruit else 0,
            "fruit_max_amount": int(30 * vegetation_factor) if has_fruit else 0,
        }

    def migration_cost_seed(self, x: int, y: int) -> MigrationCostSeed:
        """More saturated areas have more resources but are harder to migrate into/out of."""
        saturation_factor = self.__saturation(x, y) / 255
        cost = int(20 * saturation_factor)
        return {
            "migrate_in_cost": cost,
            "migrate_out_cost": cost,
        }

    def max_agents_seed(self, x: int, y: int) -> int:
        """Higher saturation means more resources, so we can support more agents."""
        saturation_factor = self.__saturation(x, y) / 255
        return int(50 * saturation_factor)

    def temperature_seed(self, x: int, y: int) -> int:
        """Calculate temperature based on hue, where redder colors are higher and therefore colder."""
        red_index = abs(
            (self.__hue(x, y) + 180) % 360 - 180
        )  # handle the 360 / 0 deg point on the circle, 0 - reddest
        temperature_factor = red_index / 180
        return int(28 * temperature_factor)

    def color_at(self, x: int, y: int) -> list[int]:
        """Get RGB color for the given cell coordinates."""
        return self.__rgb(x, y)

    def __rgb(self, x: int, y: int) -> list[int]:
        return [int(v * 255) for v in hsv_to_rgb(*(self.hsv_data[y, x, :] / 255))]

    def __hue(self, x: int, y: int) -> int:
        return int(self.hsv_data[y, x, 0])

    def __saturation(self, x: int, y: int) -> int:
        return int(self.hsv_data[y, x, 1])

    def __value(self, x: int, y: int) -> int:
        return int(self.hsv_data[y, x, 2])
