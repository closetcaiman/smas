import random
from dataclasses import dataclass

from model.constants import ACTION_WEIGHT_DECAY, MOST_PREFERRED_ACTION_WEIGHT
from model.world.elements.world_element import WorldElement

from .action import Action
from .genome import FullGenome


@dataclass
class Agent(WorldElement):
    """
    Represents an individual agent in the simulation, with its own state and behavior.

    Attributes:
        energy: int - The current energy level of the agent.
        age: int - The age of the agent in simulation steps.
        temperature: int - The current temperature experienced by the agent.
        time_since_last_breeding: int - The number of steps since the agent last reproduced.
        genome: FullGenome - The genetic makeup of the agent, determining its traits and preferences.

    Methods:
        get_wanted_action() -> Action: Determines the action the agent wants to take based on its genome and current state.
        step_simulation() -> None: Updates the agent's state for a simulation step, including energy consumption and aging.
        apply_reproduction_cost() -> None: Applies the energy cost of reproduction and resets the breeding timer.

    """

    energy: int
    age: int
    temperature: int
    time_since_last_breeding: int
    genome: FullGenome

    def get_wanted_action(self) -> Action:
        """
        Determine the action the agent wants to take based on its genome and current state.

        The agent evaluates its preferred actions in order, applying weights to create a probability distribution for action selection.
        The most preferred action is weighted the highest, and the weights decay for less preferred actions.
        The agent also checks if it meets the conditions for reproduction before including that action in the choices.

        Returns:
            Action: The action the agent has decided to take.

        """
        choices = []
        weight = MOST_PREFERRED_ACTION_WEIGHT
        for action in self.genome.preferred_action.value:
            if (
                action == Action.REPRODUCE.value
                and self.energy > self.genome.min_energy_to_reproduce.value
                and self.time_since_last_breeding > self.genome.breeding_interval.value
                and self.age > self.genome.maturity_age.value
            ):
                choices.extend([Action.REPRODUCE] * weight)
            elif action == Action.MIGRATE.value:
                choices.extend([Action.MIGRATE] * weight)
            else:
                choices.extend([Action.EAT] * weight)

            weight //= ACTION_WEIGHT_DECAY

        return random.choice(choices)

    def step_simulation(self) -> None:
        """
        Update the agent's state for a simulation step, including energy consumption and aging.

        Overrides:
            WorldElement.step_simulation: Updates the agent's energy based on its metabolic rate and age,
                and increments its age and time since last breeding. The energy cost is higher if the current temperature
        """
        temperature_hard_to_maintain = (
            abs(self.temperature - self.genome.ideal_temperature.value)
            > self.genome.temperature_tolerance.value
        )
        self.energy -= round(
            self.genome.metabolic_rate.value
            * (1 + (self.age / 500))
            * (2 if temperature_hard_to_maintain else 1)
        )
        self.age += 1
        self.time_since_last_breeding += 1

    def apply_reproduction_cost(self) -> None:
        """Apply the energy cost of reproduction and reset the breeding timer."""
        self.energy -= self.genome.min_energy_to_reproduce.value
        self.time_since_last_breeding = 0
