from abc import ABC, abstractmethod


class Genome(ABC):
    @abstractmethod
    def from_dna(self, dna: str):
        pass

    @abstractmethod
    def to_dna(self) -> str:
        pass
