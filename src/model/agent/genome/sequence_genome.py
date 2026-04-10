import dataclasses
from typing import List

from .genome import Genome


@dataclasses.dataclass
class SequenceGenome(Genome):
    value: List[int]
    length: int
    each_length: int

    def from_dna(self, dna: str) -> None:
        assert len(dna) == self.length
        self.value = []
        for i in range(0, len(dna), self.each_length):
            self.value.append(int(dna[i : i + self.each_length], 2))

    def to_dna(self) -> str:
        dna = "".join([f"{v:0{self.each_length}b}" for v in self.value])
        return dna
