from random import randrange, shuffle

from config.default import ModelConfig
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
    def create_genome(config: ModelConfig = ModelConfig()) -> FullGenome:
        """
        Generate a new FullGenome instance with randomized traits for an agent.

        Args:
            config (ModelConfig): The configuration for the simulation.

        Returns:
            FullGenome: A new genome instance with randomized traits for an agent.

        """
        return FullGenome(
            min_energy_to_reproduce=IntGenome(
                randrange(
                    config.MIN_ENERGY_TO_REPRODUCE_LOW,
                    config.MIN_ENERGY_TO_REPRODUCE_HIGH,
                ),
                16,
                config.MIN_ENERGY_TO_REPRODUCE_LOW,
                config.MIN_ENERGY_TO_REPRODUCE_HIGH,
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
                randrange(config.IDEAL_TEMPERATURE_LOW, config.IDEAL_TEMPERATURE_HIGH),
                8,
                config.IDEAL_TEMPERATURE_LOW,
                config.IDEAL_TEMPERATURE_HIGH,
            ),
            temperature_tolerance=IntGenome(
                randrange(
                    config.TEMPERATURE_TOLERANCE_LOW, config.TEMPERATURE_TOLERANCE_HIGH
                ),
                8,
                config.TEMPERATURE_TOLERANCE_LOW,
                config.TEMPERATURE_TOLERANCE_HIGH,
            ),
            metabolic_rate=IntGenome(
                randrange(config.METABOLIC_RATE_LOW, config.METABOLIC_RATE_HIGH),
                6,
                config.METABOLIC_RATE_LOW,
                config.METABOLIC_RATE_HIGH,
            ),
            maturity_age=IntGenome(
                randrange(config.MATURITY_AGE_LOW, config.MATURITY_AGE_HIGH),
                16,
                config.MATURITY_AGE_LOW,
                config.MATURITY_AGE_HIGH,
            ),
            size=IntGenome(
                randrange(config.SIZE_LOW, config.SIZE_HIGH),
                8,
                config.SIZE_LOW,
                config.SIZE_HIGH,
            ),
            breeding_interval=IntGenome(
                randrange(config.BREEDING_INTERVAL_LOW, config.BREEDING_INTERVAL_HIGH),
                8,
                config.BREEDING_INTERVAL_LOW,
                config.BREEDING_INTERVAL_HIGH,
            ),
        )

    @staticmethod
    def __shuffle(lst: list) -> list:
        shuffle(lst)
        return lst
