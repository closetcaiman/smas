import pytest

from model.agent.genome import FullGenome, IntGenome, SequenceGenome


class TestFullCombinedGenome:
    def test_initialization(self):
        genome = FullGenome(
            min_energy_to_reproduce=IntGenome(50, 16),
            preferred_food=SequenceGenome([0, 1, 2], 6, 2),
            preferred_action=SequenceGenome([0, 1, 2], 6, 2),
            ideal_temperature=IntGenome(20, 8),
            temperature_tolerance=IntGenome(5, 8),
            metabolic_rate=IntGenome(15, 6),
            maturity_age=IntGenome(30, 16),
            size=IntGenome(40, 8),
            breeding_interval=IntGenome(5, 8),
        )
        assert genome.min_energy_to_reproduce.value == 50
        assert genome.size.value == 40

    def test_total_len(self):
        genome = FullGenome(
            min_energy_to_reproduce=IntGenome(50, 16),
            preferred_food=SequenceGenome([0, 1, 2], 6, 2),
            preferred_action=SequenceGenome([0, 1, 2], 6, 2),
            ideal_temperature=IntGenome(20, 8),
            temperature_tolerance=IntGenome(5, 8),
            metabolic_rate=IntGenome(15, 6),
            maturity_age=IntGenome(30, 16),
            size=IntGenome(40, 8),
            breeding_interval=IntGenome(5, 8),
        )
        expected = 16 + 6 + 6 + 8 + 8 + 6 + 16 + 8 + 8
        assert genome.total_len() == expected

    def test_to_dna_and_back(self):
        genome = FullGenome(
            min_energy_to_reproduce=IntGenome(50, 16),
            preferred_food=SequenceGenome([0, 1, 2], 6, 2),
            preferred_action=SequenceGenome([0, 1, 2], 6, 2),
            ideal_temperature=IntGenome(20, 8),
            temperature_tolerance=IntGenome(5, 8),
            metabolic_rate=IntGenome(15, 6),
            maturity_age=IntGenome(30, 16),
            size=IntGenome(40, 8),
            breeding_interval=IntGenome(5, 8),
        )
        dna = genome.to_dna()
        genome.from_dna(dna)
        assert genome.min_energy_to_reproduce.value == 50
        assert genome.size.value == 40

    def test_from_dna_wrong_length_fails(self):
        genome = FullGenome(
            min_energy_to_reproduce=IntGenome(50, 16),
            preferred_food=SequenceGenome([0, 1, 2], 6, 2),
            preferred_action=SequenceGenome([0, 1, 2], 6, 2),
            ideal_temperature=IntGenome(20, 8),
            temperature_tolerance=IntGenome(5, 8),
            metabolic_rate=IntGenome(15, 6),
            maturity_age=IntGenome(30, 16),
            size=IntGenome(40, 8),
            breeding_interval=IntGenome(5, 8),
        )
        with pytest.raises(AssertionError):
            genome.from_dna("too_short")
