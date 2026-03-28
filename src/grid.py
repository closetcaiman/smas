import random
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
                    grass_amount=random.randrange(10, 30),
                    grass_growth=random.randrange(2, 5),
                    grass_max_amount=random.randrange(100, 200),
                    tall_grass_amount=random.randrange(100, 200),
                    tall_grass_growth=random.randrange(2, 5),
                    tall_grass_max_amount=random.randrange(100, 200),
                    fruit_amount=random.randrange(50, 100),
                    fruit_growth=random.randrange(1, 3),
                    fruit_max_amount=random.randrange(50, 100),
                    migrate_in_cost=random.randrange(10, 20),
                    migrate_out_cost=random.randrange(10, 20),
                    max_agents=random.randrange(20, 30),
                    temperature=random.randrange(0, 28),
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
