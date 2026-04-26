from abc import ABC, abstractmethod


class Genome(ABC):
    """Abstract base class for genomes, defining the interface for genetic representation and manipulation."""

    length: int

    @abstractmethod
    def from_dna(self, dna: str) -> None:
        """Initialize the genome's state from a DNA string representation."""
        raise NotImplementedError("Subclasses must implement from_dna()")

    @abstractmethod
    def to_dna(self) -> str:
        """Convert the genome's state to a DNA string representation."""
        raise NotImplementedError("Subclasses must implement to_dna()")
