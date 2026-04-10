from abc import ABC, abstractmethod


class Genome(ABC):
    length: int

    @abstractmethod
    def from_dna(self, dna: str) -> None:
        pass

    @abstractmethod
    def to_dna(self) -> str:
        pass
