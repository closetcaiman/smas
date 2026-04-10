from model.agent.genome.genome_factory import create_genome, crossover_genomes


class TestGenomeFactory:
    def test_create_genome(self):
        genome = create_genome()
        assert genome is not None
        assert genome.min_energy_to_reproduce.value >= 40
        assert genome.min_energy_to_reproduce.value < 80
        assert genome.size.value >= 20
        assert genome.size.value < 60

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
