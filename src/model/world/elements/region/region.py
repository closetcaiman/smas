from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from model.world.elements.food import FoodResources
from model.world.elements.world_element import WorldElement

if TYPE_CHECKING:
    from model.agent import Agent


@dataclass
class Region(WorldElement):
    """
    Represents a single cell in the world grid, containing food resources, agents, and other properties.

    Implements:
        WorldElement: Base class for all elements in the world, providing common functionality and interface.
    """

    food: FoodResources
    migrate_in_cost: int
    migrate_out_cost: int
    max_agents: int
    temperature: int
    neighbors: List["Region"]
    agents: List[Agent]

    coordinates: tuple[int, int]
    is_barrier: bool = False

    def step_simulation(self) -> None:
        """
        Perform one step of the simulation for this region, including updating food resources and agents.

        Overrides:
            WorldElement.step_simulation: Updates the state of the region by first updating the food resources
                and then iterating through each agent to update their state based on the current temperature of the region.
        """
        self.food.step_simulation()
        for agent in self.agents:
            agent.temperature = self.temperature
            agent.step_simulation()
