import dataclasses

from .genome import Genome


@dataclasses.dataclass
class IntGenome(Genome):
    """
    A simple genome that encodes an integer value as a binary string of fixed length.

    Implements: Genome

    Attributes:
        value: int - The integer value represented by the genome.
        length: int - The fixed length of the binary string representation of the genome.

    Methods:
        from_dna(dna: str) -> None: Initializes the genome's value from a binary string representation.
        to_dna() -> str: Converts the genome's value to a binary string representation of the specified length.

    """

    value: int
    length: int

    def from_dna(self, dna: str) -> None:
        """
        Initialize the genome's value from a binary string representation.

        Overrides:
            Genome.from_dna: Decodes the binary string into an integer based on the specified length.

        Args:
            dna: A binary string representing the genome, where the length of the string must match the specified length.

        Returns:
            None

        """
        assert len(dna) == self.length
        self.value = int(dna, 2)

    def to_dna(self) -> str:
        """
        Convert the genome's value to a binary string representation of the specified length.

        Overrides:
            Genome.to_dna: Encodes the integer into a binary string based on the specified length.

        Returns:
            A binary string representing the genome, where the length of the string matches the specified length.

        """
        return f"{self.value:0{self.length}b}"
