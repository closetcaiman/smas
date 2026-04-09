import dataclasses
from typing import List

from model.agent.agent import Agent
from model.map.food_resources import FoodResources


@dataclasses.dataclass
class Region:
    food: FoodResources
    migrate_in_cost: int
    migrate_out_cost: int
    max_agents: int
    temperature: int
    neighbors: List["Region"]
    agents: List[Agent]
    is_barrier: bool = False

    def step_simulation(self):
        self.food.step_simulation()
        for agent in self.agents:
            agent.temperature = self.temperature
            agent.step_simulation()
