import dataclasses
from typing import List

from .genome import Genome


@dataclasses.dataclass
class SequenceGenome(Genome):
    """
    A genome that encodes a sequence of integer values, where each value is represented by a fixed number of bits.

    Attributes:
        value: A list of integer values decoded from the genome.
        length: The total length of the genome in bits.
        each_length: The number of bits used to encode each individual value in the sequence.

    """

    value: List[int]
    length: int
    each_length: int

    def from_dna(self, dna: str) -> None:
        """
        Decode the binary string representation of the genome into a list of integer values.

        Overrides:
            Genome.from_dna: Decodes the binary string into a list of integers based on the specified length and each_length.

        Args:
            dna: A binary string representing the genome, where each value is encoded in a fixed number of bits.

        Returns:
            None

        """
        assert len(dna) == self.length
        self.value = []
        for i in range(0, len(dna), self.each_length):
            self.value.append(int(dna[i : i + self.each_length], 2))

    def to_dna(self) -> str:
        """
        Encode the list of integer values into a binary string representation of the genome.

        Overrides:
            Genome.to_dna: Encodes the list of integers into a binary string based on the specified length and each_length.

        Returns:
            A binary string representing the genome, where each value is encoded in a fixed number of bits.

        """
        dna = "".join([f"{v:0{self.each_length}b}" for v in self.value])
        return dna
