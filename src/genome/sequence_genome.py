import dataclasses
from typing import List

from genome.genome import Genome


@dataclasses.dataclass
class SequenceGenome(Genome):
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
