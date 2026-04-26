import pytest

from model.agent.genome.sequence_genome import SequenceGenome


class TestSequenceGenome:
    def test_initialization(self):
        genome = SequenceGenome(value=[1, 2, 3], length=6, each_length=2)
        assert genome.value == [1, 2, 3]
        assert genome.length == 6
        assert genome.each_length == 2

    def test_from_dna(self):
        genome = SequenceGenome(value=[], length=6, each_length=2)
        genome.from_dna("011011")
        assert genome.value == [1, 2, 3]

    def test_to_dna(self):
        genome = SequenceGenome(value=[1, 2, 3], length=6, each_length=2)
        assert genome.to_dna() == "011011"

    def test_dna_length_validation(self):
        genome = SequenceGenome(value=[], length=6, each_length=2)
        with pytest.raises(AssertionError):
            genome.from_dna("010")
