import dataclasses
from typing import List

from agent import Agent
from enums import FoodType


@dataclasses.dataclass
class Region:
    grass_amount: int
    grass_max_amount: int
    grass_growth: int

    tall_grass_amount: int
    tall_grass_max_amount: int
    tall_grass_growth: int

    fruit_amount: int
    fruit_max_amount: int
    fruit_growth: int

    migrate_in_cost: int
    migrate_out_cost: int
    max_agents: int

    temperature: int

    neighbors: List["Region"]
    agents: List["Agent"]

    is_barrier: bool = False

    def step_simulation(self):
        self.grass_amount = min(
            self.grass_amount + self.grass_growth, self.grass_max_amount
        )
        self.tall_grass_amount = min(
            self.tall_grass_amount + self.tall_grass_growth, self.tall_grass_max_amount
        )
        self.fruit_amount = min(
            self.fruit_amount + self.fruit_growth, self.fruit_max_amount
        )
        for agent in self.agents:
            agent.temperature = self.temperature
            agent.step_simulation()


def energy_amount_from_food(food: FoodType):
    match food:
        case FoodType.GRASS:
            return 10
        case FoodType.TALL_GRASS:
            return 15
        case FoodType.FRUIT:
            return 30
