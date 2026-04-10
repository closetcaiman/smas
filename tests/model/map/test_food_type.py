from model.map.food_type import FoodType


class TestFoodType:
    def test_food_type_values(self):
        assert FoodType.GRASS.value == 0
        assert FoodType.TALL_GRASS.value == 1
        assert FoodType.FRUIT.value == 2

    def test_energy_amount_grass(self):
        assert FoodType.GRASS.energy_amount() == 10

    def test_energy_amount_tall_grass(self):
        assert FoodType.TALL_GRASS.energy_amount() == 15

    def test_energy_amount_fruit(self):
        assert FoodType.FRUIT.energy_amount() == 30
