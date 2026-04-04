import random

from action import Action
from food_type import FoodType
from genome.full_combined_genome import FullCombinedGenome
from genome.int_genome import IntGenome
from genome.sequence_genome import SequenceGenome


def make_starting_genome():
    return FullCombinedGenome(
        min_energy_to_reproduce=IntGenome(random.randrange(40, 80), 16),
        preferred_food=SequenceGenome(
            shuffled(
                [FoodType.GRASS.value, FoodType.TALL_GRASS.value, FoodType.FRUIT.value]
            ),
            6,
            2,
        ),
        preferred_action=SequenceGenome(
            shuffled([Action.EAT.value, Action.REPRODUCE.value, Action.MIGRATE.value]),
            6,
            2,
        ),
        ideal_temperature=IntGenome(random.randrange(0, 28), 8),
        temperature_tolerance=IntGenome(random.randrange(4, 10), 8),
        metabolic_rate=IntGenome(random.randrange(10, 30), 6),
        maturity_age=IntGenome(random.randrange(20, 40), 16),
        size=IntGenome(random.randrange(20, 60), 8),
        breeding_interval=IntGenome(random.randrange(2, 20), 8),
    )


def shuffled(values: list):
    random.shuffle(values)
    return values


def cross_genomes(a: FullCombinedGenome, b: FullCombinedGenome) -> FullCombinedGenome:
    a_dna = a.to_dna()
    b_dna = b.to_dna()

    if random.random() > 0.5:
        a_dna, b_dna = b_dna, a_dna

    cut1 = round(random.uniform(0, len(a_dna) // 2))
    cut2 = round(random.uniform(cut1, len(a_dna)))

    child_genome = make_starting_genome()
    child_genome.from_dna(a_dna[:cut1] + b_dna[cut1:cut2] + a_dna[cut2:])
    return child_genome
