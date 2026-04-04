import dataclasses
import random
from typing import List

from enums import Action, FoodType


@dataclasses.dataclass
class IntGenome:
    value: int
    size: int

    def from_dna(self, dna: str):
        assert len(dna) == self.size
        self.value = int(dna, 2)

    def to_dna(self):
        return f"{self.value:0{self.size}b}"


@dataclasses.dataclass
class SequenceGenome:
    value: List[int]
    size: int
    each_size: int

    def from_dna(self, dna: str):
        assert len(dna) == self.size
        self.value = []
        for i in range(0, len(dna), self.each_size):
            self.value.append(int(dna[i : i + self.each_size], 2))

    def to_dna(self):
        dna = "".join([f"{v:0{self.each_size}b}" for v in self.value])
        return dna


@dataclasses.dataclass
class Genome:
    min_energy_to_reproduce: IntGenome
    preferred_food: SequenceGenome
    preferred_action: SequenceGenome
    ideal_temperature: IntGenome
    temperature_tolerance: IntGenome
    metabolic_rate: IntGenome
    maturity_age: IntGenome
    size: IntGenome
    breeding_interval: IntGenome

    def _all_parts(self):
        return [
            self.min_energy_to_reproduce,
            self.preferred_food,
            self.preferred_action,
            self.ideal_temperature,
            self.temperature_tolerance,
            self.metabolic_rate,
            self.maturity_age,
            self.size,
            self.breeding_interval,
        ]

    def total_len(self):
        return sum([p.size for p in self._all_parts()])

    def from_dna(self, dna: str):
        assert len(dna) == self.total_len()
        i = 0
        for p in self._all_parts():
            p.from_dna(dna[i : i + p.size])
            i += p.size

    def to_dna(self):
        return "".join([p.to_dna() for p in self._all_parts()])


def make_starting_genome():
    return Genome(
        min_energy_to_reproduce=IntGenome(random.randrange(40, 80), 16),
        preferred_food=SequenceGenome(
            shuffled(
                [FoodType.GRASS.value, FoodType.TALL_GRASS.value, FoodType.FRUIT.value]
            ),
            6,
            2,
        ),
        preferred_action=SequenceGenome(
            shuffled([Action.EAT.value, Action.REPRODUCE.value, Action.MIGRATE.value]),
            6,
            2,
        ),
        ideal_temperature=IntGenome(random.randrange(0, 28), 8),
        temperature_tolerance=IntGenome(random.randrange(4, 10), 8),
        metabolic_rate=IntGenome(random.randrange(10, 30), 6),
        maturity_age=IntGenome(random.randrange(20, 40), 16),
        size=IntGenome(random.randrange(20, 60), 8),
        breeding_interval=IntGenome(random.randrange(2, 20), 8),
    )


def shuffled(values: list):
    random.shuffle(values)
    return values


def cross_genomes(a: Genome, b: Genome) -> Genome:
    a_dna = a.to_dna()
    b_dna = b.to_dna()

    if random.random() > 0.5:
        a_dna, b_dna = b_dna, a_dna

    cut1 = round(random.uniform(0, len(a_dna) // 2))
    cut2 = round(random.uniform(cut1, len(a_dna)))

    child_genome = make_starting_genome()
    child_genome.from_dna(a_dna[:cut1] + b_dna[cut1:cut2] + a_dna[cut2:])
    return child_genome
