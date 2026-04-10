import pytest

from model.agent.genome.int_genome import IntGenome


class TestIntGenome:
    def test_initialization(self):
        genome = IntGenome(value=10, size=8)
        assert genome.value == 10
        assert genome.size == 8

    def test_from_dna(self):
        genome = IntGenome(value=0, size=8)
        genome.from_dna("00001010")
        assert genome.value == 10

    def test_to_dna(self):
        genome = IntGenome(value=10, size=8)
        assert genome.to_dna() == "00001010"

    def test_from_dna_full_range(self):
        genome = IntGenome(value=0, size=8)
        genome.from_dna("11111111")
        assert genome.value == 255

    def test_dna_length_validation(self):
        genome = IntGenome(value=0, size=8)
        with pytest.raises(AssertionError):
            genome.from_dna("1111")
