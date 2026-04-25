from typing import Iterator, List

from model.map.food_resources import FoodResources
from model.map.map_image_sampler import MapImageSampler
from model.map.region import Region


class Grid:
    _data: List[List[Region]]
    _width: int
    _height: int

    def __init__(self, sampler: MapImageSampler, width: int, height: int) -> None:
        self._data = [[] for _ in range(height)]
        self._width = width
        self._height = height
        self._sampler = sampler

        for i in range(self._height):
            for j in range(self._width):
                green_index = abs(
                    self._sampler.hue(i, j) - 120
                )  # 120 - angle for green, green_index == 0 -> greenest
                vegetation_factor = max(0, 60 - green_index) / 60
                saturation_factor = self._sampler.saturation(i, j) / 255
                light_factor = max(0, self._sampler.value(i, j) - 215) / 40
                has_tall_grass = saturation_factor > 0.3
                has_fruit = saturation_factor > 0.5
                red_index = abs(
                    (self._sampler.hue(i, j) + 180) % 360 - 180
                )  # handle the 360 / 0 deg point on the circle, 0 - reddest
                temperature_factor = 1 - red_index / 180
                self._data[i].append(
                    Region(
                        food=FoodResources(
                            grass_amount=int(20 * vegetation_factor),
                            grass_growth=int(10 * light_factor),
                            grass_max_amount=int(50 * vegetation_factor),
                            tall_grass_amount=int(10 * vegetation_factor)
                            if has_tall_grass
                            else 0,
                            tall_grass_growth=int(10 * light_factor)
                            if has_tall_grass
                            else 0,
                            tall_grass_max_amount=int(30 * vegetation_factor)
                            if has_tall_grass
                            else 0,
                            fruit_amount=int(10 * vegetation_factor)
                            if has_fruit
                            else 0,
                            fruit_growth=int(10 * light_factor) if has_fruit else 0,
                            fruit_max_amount=int(30 * vegetation_factor)
                            if has_fruit
                            else 0,
                        ),
                        migrate_in_cost=int(20 * saturation_factor),
                        migrate_out_cost=int(20 * saturation_factor),
                        max_agents=int(50 * saturation_factor),
                        temperature=int(28 * temperature_factor),
                        neighbors=[],
                        agents=[],
                    )
                )

        for i in range(self._height):
            for j in range(self._width):
                if i > 0:
                    self._data[i][j].neighbors.append(self._data[i - 1][j])
                if i + 1 < self._height:
                    self._data[i][j].neighbors.append(self._data[i + 1][j])
                if j > 0:
                    self._data[i][j].neighbors.append(self._data[i][j - 1])
                if j + 1 < self._width:
                    self._data[i][j].neighbors.append(self._data[i][j + 1])

    @property
    def regions(self) -> Iterator[Region]:
        for row in self._data:
            for region in row:
                yield region

    def color_at(self, x, y):
        return self._sampler.rgb(x, y)
