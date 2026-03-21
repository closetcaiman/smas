from typing import List
from region import Region

class Grid:
    _data: List[List[Region]]
    _width: int
    _height: int

    def __init__(self, width: int, height: int):
        self._data = [[] for _ in range(height)]
        self._width = width
        self._height = height

        for i in range(self._height):
            for j in range(self._width):
                self._data[i].append(Region(
                    grass_amount=20,
                    grass_growth=1,
                    grass_max_amount=100,
                    tall_grass_amount=10,
                    tall_grass_growth=1,
                    tall_grass_max_amount=100,
                    fruit_amount=30,
                    fruit_growth=1,
                    fruit_max_amount=100,
                    migrate_in_cost=50,
                    migrate_out_cost=50,
                    max_agents=10,
                    neighbors=[],
                    agents=[],
                ))

        for i in range(self._height):
            for j in range(self._width):
                if i > 0:
                    self._data[i][j].neighbors.append(self._data[i-1][j])
                if i+1 < self._height:
                    self._data[i][j].neighbors.append(self._data[i+1][j])
                if j > 0:
                    self._data[i][j].neighbors.append(self._data[i][j-1])
                if j+1 < self._width:
                    self._data[i][j].neighbors.append(self._data[i][j+1])

    def regions(self):
        return (region for row in self._data for region in row)
