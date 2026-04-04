import dataclasses

from genome.genome import Genome


@dataclasses.dataclass
class IntGenome(Genome):
    value: int
    size: int

    def from_dna(self, dna: str):
        assert len(dna) == self.size
        self.value = int(dna, 2)

    def to_dna(self):
        return f"{self.value:0{self.size}b}"
