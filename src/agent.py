import dataclasses
import random

from action import Action
from genome.full_combined_genome import FullCombinedGenome

MOST_PREFERRED_ACTION_WEIGHT = 6
ACTION_WEIGHT_DECAY = 2


@dataclasses.dataclass
class Agent:
    energy: int
    age: int
    temperature: int
    time_since_last_breeding: int
    genome: FullCombinedGenome

    def get_wanted_action(self):
        """
        Returns the action that the agent wants to do.
        It is selected at random from possible actions
        with probability weighted by actor's preference.
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

    def step_simulation(self):
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

    def apply_reproduction_cost(self):
        self.energy -= self.genome.min_energy_to_reproduce.value
        self.time_since_last_breeding = 0
