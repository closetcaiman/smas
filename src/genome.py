import random
from typing import List
import dataclasses

from enums import Food, Action


@dataclasses.dataclass
class IntGenome:
    value: int
    size: int

    def from_dna(self, v):
        assert len(v) == self.size
        self.value = int(v, 2)

    def to_dna(self):
        return f"{self.value:0{self.size}b}"


@dataclasses.dataclass
class SequenceGenome:
    value: List[int]
    size: int
    each_size: int

    def from_dna(self, v):
        assert len(v) == self.size
        count = len(v) // self.each_size
        self.value = []
        for i in range(0, len(v), count):
            self.value.append(int(v[i:i+self.each_size], 2))

    def to_dna(self):
        return "".join([f"{v:0{self.each_size}b}" for v in self.value])


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
            self.breeding_interval
        ]

    def total_len(self):
        return sum([p.size for p in self._all_parts()])

    def from_dna(self, v):
        assert len(v) == self.total_len()
        i = 0
        for p in self._all_parts():
            p.from_dna(v[i:i+p.size])
            i += p.size

    def to_dna(self):
        return "".join([p.to_dna() for p in self._all_parts()])


def make_starting_genome():
    return Genome(
        min_energy_to_reproduce=IntGenome(50, 16),
        preferred_food=SequenceGenome([Food.GRASS.value, Food.TALL_GRASS.value, Food.FRUIT.value], 6, 2),
        preferred_action=SequenceGenome([Action.EAT.value, Action.REPRODUCE.value, Action.MIGRATE.value], 6, 2),
        ideal_temperature=IntGenome(20, 8),
        temperature_tolerance=IntGenome(20, 8),
        metabolic_rate=IntGenome(2, 6),
        maturity_age=IntGenome(40, 16),
        size=IntGenome(40, 8),
        breeding_interval=IntGenome(10, 8),
    )

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