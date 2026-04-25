from model.agent.genome import GenomeFactory


class TestGenomeFactory:
    def test_create_genome(self):
        genome = GenomeFactory.create_genome()
        assert genome is not None
        assert genome.min_energy_to_reproduce.value >= 40
        assert genome.min_energy_to_reproduce.value < 80
        assert genome.size.value >= 20
        assert genome.size.value < 60
