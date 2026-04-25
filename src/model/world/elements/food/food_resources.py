import dataclasses

from model.world.elements.world_element import WorldElement


@dataclasses.dataclass
class FoodResources(WorldElement):
    """Represents the food resources available in a region, including grass, tall grass, and fruit."""

    grass_amount: int
    grass_max_amount: int
    grass_growth: int

    tall_grass_amount: int
    tall_grass_max_amount: int
    tall_grass_growth: int

    fruit_amount: int
    fruit_max_amount: int
    fruit_growth: int

    def step_simulation(self) -> None:
        """
        Perform one step of the simulation for this food resource, including growth of grass, tall grass, and fruit.

        Ovverrides:
            WorldElement.step_simulation: Updates the amounts of grass, tall grass,
                and fruit based on their respective growth rates, ensuring that the amounts do not exceed their maximum limits.
        """
        self.grass_amount = min(
            self.grass_amount + self.grass_growth, self.grass_max_amount
        )
        self.tall_grass_amount = min(
            self.tall_grass_amount + self.tall_grass_growth, self.tall_grass_max_amount
        )
        self.fruit_amount = min(
            self.fruit_amount + self.fruit_growth, self.fruit_max_amount
        )
