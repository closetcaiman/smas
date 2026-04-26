import dataclasses

from .genome import Genome
from .int_genome import IntGenome
from .sequence_genome import SequenceGenome


@dataclasses.dataclass
class FullGenome(Genome):
    """
    Represents the complete genetic makeup of an agent, consisting of multiple traits encoded as IntGenome and SequenceGenome instances.

    Attributes:
        min_energy_to_reproduce: An IntGenome representing the minimum energy required for the agent to reproduce.
        preferred_food: A SequenceGenome representing the agent's preferred types of food.
        preferred_action: A SequenceGenome representing the agent's preferred actions.
        ideal_temperature: An IntGenome representing the agent's ideal temperature for survival.
        temperature_tolerance: An IntGenome representing the agent's tolerance to temperature variations.
        metabolic_rate: An IntGenome representing the agent's metabolic rate, affecting energy consumption.
        maturity_age: An IntGenome representing the age at which the agent reaches maturity and can reproduce.
        size: An IntGenome representing the physical size of the agent, which may affect its interactions with the environment and other agents.
        breeding_interval: An IntGenome representing the number of time steps between breeding opportunities for the agent.

    Methods:
        total_len() -> int: Calculates the total length of the genome by summing the lengths of all individual genome parts.
        from_dna(dna: str) -> None: Initializes the genome's traits from a binary string representation by delegating to each individual genome part.
        to_dna() -> str: Converts the genome's traits into a binary string representation by concatenating the DNA representations of all individual genome parts.

    """

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
        """
        Calculate the total length of the genome by summing the lengths of all individual genome parts.

        Returns:
            The total length of the genome in bits, which is the sum of the lengths of all individual genome parts.

        """
        return sum([p.length for p in self.__all_parts()])

    def from_dna(self, dna: str) -> None:
        """
        Initialize the genome's traits from a binary string representation by delegating to each individual genome part.

        Overrides:
            Genome.from_dna: Decodes the binary string into the respective traits of the genome by calling from_dna on each individual genome part.

        Args:
            dna: A binary string representing the entire genome, where the length of the string must match the total length of the genome.

        Returns:
            None

        """
        assert len(dna) == self.total_len()
        i = 0
        for p in self.__all_parts():
            p.from_dna(dna[i : i + p.length])
            i += p.length

    def to_dna(self) -> str:
        """
        Convert the genome's traits into a binary string representation by concatenating the DNA representations of all individual genome parts.

        Overrides:
            Genome.to_dna: Encodes the respective traits of the genome into a binary string by calling to_dna on each individual genome part.

        Returns:
            A binary string representing the entire genome, where the length of the string matches the total length of the genome.

        """
        return "".join([p.to_dna() for p in self.__all_parts()])
