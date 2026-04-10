import dataclasses

from .genome import Genome
from .int_genome import IntGenome
from .sequence_genome import SequenceGenome


@dataclasses.dataclass
class FullCombinedGenome(Genome):
    min_energy_to_reproduce: IntGenome
    preferred_food: SequenceGenome
    preferred_action: SequenceGenome
    ideal_temperature: IntGenome
    temperature_tolerance: IntGenome
    metabolic_rate: IntGenome
    maturity_age: IntGenome
    size: IntGenome
    breeding_interval: IntGenome

    def __all_parts(self) -> list[Genome]:
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

    def total_len(self) -> int:
        return sum([p.length for p in self.__all_parts()])

    def from_dna(self, dna: str) -> None:
        assert len(dna) == self.total_len()
        i = 0
        for p in self.__all_parts():
            p.from_dna(dna[i : i + p.length])
            i += p.length

    def to_dna(self) -> str:
        return "".join([p.to_dna() for p in self.__all_parts()])
