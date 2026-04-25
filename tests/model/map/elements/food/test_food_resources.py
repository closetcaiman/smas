from model.world import FoodResources


class TestFoodResources:
    def test_initialization(self):
        food = FoodResources(
            grass_amount=50,
            grass_max_amount=100,
            grass_growth=5,
            tall_grass_amount=50,
            tall_grass_max_amount=100,
            tall_grass_growth=5,
            fruit_amount=25,
            fruit_max_amount=50,
            fruit_growth=2,
        )
        assert food.grass_amount == 50
        assert food.tall_grass_amount == 50
        assert food.fruit_amount == 25

    def test_step_simulation_grows_resources(self):
        food = FoodResources(
            grass_amount=10,
            grass_max_amount=100,
            grass_growth=5,
            tall_grass_amount=10,
            tall_grass_max_amount=100,
            tall_grass_growth=5,
            fruit_amount=5,
            fruit_max_amount=50,
            fruit_growth=2,
        )
        food.step_simulation()
        assert food.grass_amount == 15
        assert food.tall_grass_amount == 15
        assert food.fruit_amount == 7

    def test_step_simulation_caps_at_max(self):
        food = FoodResources(
            grass_amount=98,
            grass_max_amount=100,
            grass_growth=5,
            tall_grass_amount=98,
            tall_grass_max_amount=100,
            tall_grass_growth=5,
            fruit_amount=49,
            fruit_max_amount=50,
            fruit_growth=2,
        )
        food.step_simulation()
        assert food.grass_amount == 100
        assert food.tall_grass_amount == 100
        assert food.fruit_amount == 50
