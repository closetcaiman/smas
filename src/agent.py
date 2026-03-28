import random
import dataclasses
from enums import Action
from genome import Genome


@dataclasses.dataclass
class Agent:
    energy: int
    age: int
    temperature: int
    time_since_last_breeding: int
    genome: Genome

    def wants_action(self):
        choices = []
        weight = 6
        for action in self.genome.preferred_action.value:
            if action == Action.REPRODUCE.value \
                and self.energy > self.genome.min_energy_to_reproduce.value \
                and self.time_since_last_breeding > self.genome.breeding_interval.value \
                and self.age > self.genome.maturity_age.value:
                choices.extend([Action.REPRODUCE] * weight)
            elif action == Action.MIGRATE.value:
                choices.extend([Action.MIGRATE] * weight)
            else:
                choices.extend([Action.EAT] * weight)

            weight //= 2

        return random.choice(choices)

    def step_simulation(self):
        temperature_hard_to_maintain = abs(self.temperature - self.genome.ideal_temperature.value) > self.genome.temperature_tolerance.value
        self.energy -= round(self.genome.metabolic_rate.value * (1 + (self.age / 500)) * (2 if temperature_hard_to_maintain else 1))
        self.age += 1
        self.time_since_last_breeding += 1

    def apply_reproduction_cost(self):
        self.energy -= self.genome.min_energy_to_reproduce.value
        self.time_since_last_breeding = 0