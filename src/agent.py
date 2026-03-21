import random
import dataclasses
from enums import Action
from genome import Genome


@dataclasses.dataclass
class Agent:
    energy: int
    age: int
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

    def calc_migration_cost(self, in_cost: int, out_cost: int):
        return (in_cost + out_cost) * (1 + self.age / 100)