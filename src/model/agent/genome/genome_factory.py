from random import randrange, shuffle

from model.agent.action import Action
from model.world import FoodType

from .full_genome import FullGenome
from .int_genome import IntGenome
from .sequence_genome import SequenceGenome


class GenomeFactory:
    """
    Factory class for creating new genomes with randomized traits for agents in the simulation.

    Methods:
        create_genome() -> FullGenome: Generates a new FullGenome instance with randomized traits for an agent.

    """

    @staticmethod
    def create_genome() -> FullGenome:
        """
        Generate a new FullGenome instance with randomized traits for an agent.

        Returns:
            FullGenome: A new genome instance with randomized traits for an agent.

        """
        return FullGenome(
            min_energy_to_reproduce=IntGenome(randrange(40, 80), 16),
            preferred_food=SequenceGenome(
                GenomeFactory.__shuffle(
                    [
                        FoodType.GRASS.value,
                        FoodType.TALL_GRASS.value,
                        FoodType.FRUIT.value,
                    ]
                ),
                6,
                2,
            ),
            preferred_action=SequenceGenome(
                GenomeFactory.__shuffle(
                    [Action.EAT.value, Action.REPRODUCE.value, Action.MIGRATE.value]
                ),
                6,
                2,
            ),
            ideal_temperature=IntGenome(randrange(0, 28), 8),
            temperature_tolerance=IntGenome(randrange(4, 10), 8),
            metabolic_rate=IntGenome(randrange(10, 30), 6),
            maturity_age=IntGenome(randrange(20, 40), 16),
            size=IntGenome(randrange(20, 60), 8),
            breeding_interval=IntGenome(randrange(2, 20), 8),
        )

    @staticmethod
    def __shuffle(lst: list) -> list:
        shuffle(lst)
        return lst
