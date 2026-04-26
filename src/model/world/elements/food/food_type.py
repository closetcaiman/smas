from enum import Enum


class FoodType(Enum):
    """
    Enumeration of different food types available in the world.

    Possible values:
        GRASS: Basic food type providing a small amount of energy.
        TALL_GRASS: More nutritious food type providing a moderate amount of energy.
        FRUIT: Highly nutritious food type providing a large amount of energy.

    Methods:
        energy_amount(): Return the energy amount provided by this food type.

    """

    GRASS = 0
    TALL_GRASS = 1
    FRUIT = 2

    def energy_amount(self) -> int:
        """Return the energy amount provided by this food type."""
        match self:
            case FoodType.GRASS:
                return 10
            case FoodType.TALL_GRASS:
                return 15
            case FoodType.FRUIT:
                return 30
            case _:
                raise ValueError(f"Unknown food type: {self}")
