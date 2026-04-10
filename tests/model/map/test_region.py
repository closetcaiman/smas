from model.map.food_resources import FoodResources
from model.map.region import Region


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
