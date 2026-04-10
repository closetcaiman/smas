import dataclasses


@dataclasses.dataclass
class FoodResources:
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
        self.grass_amount = min(
            self.grass_amount + self.grass_growth, self.grass_max_amount
        )
        self.tall_grass_amount = min(
            self.tall_grass_amount + self.tall_grass_growth, self.tall_grass_max_amount
        )
        self.fruit_amount = min(
            self.fruit_amount + self.fruit_growth, self.fruit_max_amount
        )
