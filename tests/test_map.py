from model.map.food_resources import FoodResources
from model.map.grid import Grid
from model.map.region import Region


class TestGrid:
    def test_initialization(self):
        grid = Grid(width=5, height=5)
        assert grid._width == 5
        assert grid._height == 5

    def test_regions_count(self):
        grid = Grid(width=3, height=4)
        regions = list(grid.regions)
        assert len(regions) == 12

    def test_regions_property_yields_all_regions(self):
        grid = Grid(width=2, height=2)
        regions = list(grid.regions)
        assert all(isinstance(r, Region) for r in regions)

    def test_neighbors_connected(self):
        grid = Grid(width=3, height=3)
        center_region = grid._data[1][1]
        assert len(center_region.neighbors) == 4

    def test_corner_has_2_neighbors(self):
        grid = Grid(width=3, height=3)
        corner_region = grid._data[0][0]
        assert len(corner_region.neighbors) == 2

    def test_edge_has_3_neighbors(self):
        grid = Grid(width=3, height=3)
        edge_region = grid._data[0][1]
        assert len(edge_region.neighbors) == 3


class TestRegion:
    def test_initialization(self):
        region = Region(
            food=FoodResources(
                grass_amount=50,
                grass_max_amount=100,
                grass_growth=5,
                tall_grass_amount=50,
                tall_grass_max_amount=100,
                tall_grass_growth=5,
                fruit_amount=25,
                fruit_max_amount=50,
                fruit_growth=2,
            ),
            migrate_in_cost=10,
            migrate_out_cost=10,
            max_agents=20,
            temperature=20,
            neighbors=[],
            agents=[],
        )
        assert region.migrate_in_cost == 10
        assert region.max_agents == 20
        assert region.temperature == 20
        assert len(region.agents) == 0

    def test_step_simulation_updates_food(self):
        region = Region(
            food=FoodResources(
                grass_amount=10,
                grass_max_amount=100,
                grass_growth=5,
                tall_grass_amount=10,
                tall_grass_max_amount=100,
                tall_grass_growth=5,
                fruit_amount=5,
                fruit_max_amount=50,
                fruit_growth=2,
            ),
            migrate_in_cost=10,
            migrate_out_cost=10,
            max_agents=20,
            temperature=20,
            neighbors=[],
            agents=[],
        )
        region.step_simulation()
        assert region.food.grass_amount == 15
