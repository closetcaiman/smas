from model.agent.genome.genome_factory import create_genome, crossover_genomes


class TestGenomeFactory:
    def test_crossover_genomes_creates_valid_child(self):
        parent1 = create_genome()
        parent2 = create_genome()
        child = crossover_genomes(parent1, parent2)
        assert child is not None
        assert child.total_len() == parent1.total_len()
        assert isinstance(child.min_energy_to_reproduce.value, int)

    def test_crossover_preserves_dna_length(self):
        parent1 = create_genome()
        parent2 = create_genome()
        child = crossover_genomes(parent1, parent2)
        assert child.total_len() == parent1.total_len()

    def test_child_dna_contains_genes_from_parents(self):
        parent1 = create_genome()
        parent2 = create_genome()
        child = crossover_genomes(parent1, parent2)
        child_dna = child.to_dna()
        assert len(child_dna) == parent1.total_len()
