from model.agent import Breeder, GenomeFactory


class TestBreeder:
    def test_crossover_genomes_creates_valid_child(self):
        parent1 = GenomeFactory.create_genome()
        parent2 = GenomeFactory.create_genome()
        child = Breeder.crossover_genomes(parent1, parent2)
        assert child is not None
        assert child.total_len() == parent1.total_len()
        assert isinstance(child.min_energy_to_reproduce.value, int)

    def test_crossover_preserves_dna_length(self):
        parent1 = GenomeFactory.create_genome()
        parent2 = GenomeFactory.create_genome()
        child = Breeder.crossover_genomes(parent1, parent2)
        assert child.total_len() == parent1.total_len()
