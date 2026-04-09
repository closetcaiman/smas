from enum import Enum


class FoodType(Enum):
    GRASS = 0
    TALL_GRASS = 1
    FRUIT = 2

    def energy_amount(self):
        match self:
            case FoodType.GRASS:
                return 10
            case FoodType.TALL_GRASS:
                return 15
            case FoodType.FRUIT:
                return 30
        assert False
