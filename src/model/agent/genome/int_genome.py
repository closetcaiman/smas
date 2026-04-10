import dataclasses

from .genome import Genome


@dataclasses.dataclass
class IntGenome(Genome):
    value: int
    length: int

    def from_dna(self, dna: str) -> None:
        assert len(dna) == self.length
        self.value = int(dna, 2)

    def to_dna(self) -> str:
        return f"{self.value:0{self.length}b}"
