from random import randrange, shuffle

from model.agent.action import Action
from model.world import FoodType

from . import config as cfg
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
            min_energy_to_reproduce=IntGenome(
                randrange(
                    cfg.MIN_ENERGY_TO_REPRODUCE_LOW, cfg.MIN_ENERGY_TO_REPRODUCE_HIGH
                ),
                16,
                cfg.MIN_ENERGY_TO_REPRODUCE_LOW,
                cfg.MIN_ENERGY_TO_REPRODUCE_HIGH,
            ),
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
            ideal_temperature=IntGenome(
                randrange(cfg.IDEAL_TEMPERATURE_LOW, cfg.IDEAL_TEMPERATURE_HIGH),
                8,
                cfg.IDEAL_TEMPERATURE_LOW,
                cfg.IDEAL_TEMPERATURE_HIGH,
            ),
            temperature_tolerance=IntGenome(
                randrange(
                    cfg.TEMPERATURE_TOLERANCE_LOW, cfg.TEMPERATURE_TOLERANCE_HIGH
                ),
                8,
                cfg.TEMPERATURE_TOLERANCE_LOW,
                cfg.TEMPERATURE_TOLERANCE_HIGH,
            ),
            metabolic_rate=IntGenome(
                randrange(cfg.METABOLIC_RATE_LOW, cfg.METABOLIC_RATE_HIGH),
                6,
                cfg.METABOLIC_RATE_LOW,
                cfg.METABOLIC_RATE_HIGH,
            ),
            maturity_age=IntGenome(
                randrange(cfg.MATURITY_AGE_LOW, cfg.MATURITY_AGE_HIGH),
                16,
                cfg.MATURITY_AGE_LOW,
                cfg.MATURITY_AGE_HIGH,
            ),
            size=IntGenome(
                randrange(cfg.SIZE_LOW, cfg.SIZE_HIGH), 8, cfg.SIZE_LOW, cfg.SIZE_HIGH
            ),
            breeding_interval=IntGenome(
                randrange(cfg.BREEDING_INTERVAL_LOW, cfg.BREEDING_INTERVAL_HIGH),
                8,
                cfg.BREEDING_INTERVAL_LOW,
                cfg.BREEDING_INTERVAL_HIGH,
            ),
        )

    @staticmethod
    def __shuffle(lst: list) -> list:
        shuffle(lst)
        return lst
