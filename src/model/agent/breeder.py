from math import floor
from random import random, uniform

from config.default import ModelConfig
from model.agent.genome import FullGenome, GenomeFactory


class Breeder:
    """
    Provides functionality for breeding agents by combining their genomes to create offspring with inherited traits.

    Methods:
        crossover_genomes(a: FullCombinedGenome, b: FullCombinedGenome) -> FullCombinedGenome:
            -> Combines the genomes of two parent agents to create a new genome for an offspring agent.

    """

    @staticmethod
    def crossover_genomes(
        a: FullGenome, b: FullGenome, config: ModelConfig = ModelConfig()
    ) -> FullGenome:
        """
        Combine the genomes of two parent agents to create a new genome for an offspring agent.

        The method takes the DNA representations of both parent genomes,
        randomly decides which parent's DNA will be the primary source,
        and then performs a crossover by selecting two random cut points.
        The resulting child genome is created by combining segments of
        the parent DNA according to these cut points.

        Args:
            a (FullCombinedGenome): The genome of the first parent agent.
            b (FullCombinedGenome): The genome of the second parent agent.
            config (ModelConfig): The configuration for the simulation.

        Returns:
            FullCombinedGenome: A new genome instance representing the offspring agent, derived from the parent genomes

        """
        a_dna = a.to_dna()
        b_dna = b.to_dna()

        if random() > 0.5:
            a_dna, b_dna = b_dna, a_dna

        cut1 = round(uniform(0, len(a_dna) // 2))
        cut2 = round(uniform(cut1, len(a_dna)))

        child_genome = GenomeFactory.create_genome()
        genome_str = a_dna[:cut1] + b_dna[cut1:cut2] + a_dna[cut2:]

        if random() > 0.95:
            genome_str = Breeder.__flip_bits_mutation(genome_str)

        child_genome.from_dna(genome_str)
        return child_genome

    @staticmethod
    def __flip_bits_mutation(genome_str: str):
        mutation_position = floor(uniform(0, len(genome_str)))
        return (
            genome_str[:mutation_position]
            + ("0" if genome_str[mutation_position] == "1" else "1")
            + genome_str[mutation_position + 1 :]
        )
