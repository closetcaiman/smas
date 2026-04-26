"""
The SimulationMediator class serves as a central hub for communication between different components of the simulation.

It allows for decoupled interactions between the data bank, logger ensuring that changes in one component do not directly affect others.
The mediator handles events such as births and deaths of agents, dispatching relevant information to the appropriate components for recording and logging.
"""

from typing import Optional

from controller.mediator.simulation_data_bank import SimulationDataBank
from controller.mediator.simulation_logger import SimulationLogger
from controller.types.data import RegionCoordinates


class SimulationMediator:
    """
    Central hub for communication between simulation components.

    Methods:
        record_birth(epoch, count, region_coordinates): Handle birth events by updating the data bank and logger.
        record_death(epoch, count, region_coordinates): Handle death events by updating the data bank and logger.

    """

    def __init__(
        self,
        databank: SimulationDataBank,
        logger: Optional[SimulationLogger] = None,
    ) -> None:
        """
        Initialize the mediator with references to the data bank and logger.

        Args:
            databank: The SimulationDataBank instance for recording historical data.
            logger: An optional SimulationLogger instance for logging events.

        Returns:
            None

        """
        self.databank = databank
        self.logger = logger

    def record_birth(
        self, epoch: int, count: int, region_coordinates: RegionCoordinates
    ) -> None:
        """
        Handle birth events by updating the data bank and logger.

        Args:
            epoch: The current epoch of the simulation.
            count: The number of agents born.
            region_coordinates: The coordinates of the region where the birth occurred.

        Returns:
            None

        """
        # Dispatch to the databank for historical tracking
        self.databank.record_births(epoch, region_coordinates, count)

        # Dispatch to the logger for a text-based trail
        if self.logger:
            self.logger.info(f"{count} agents born in {region_coordinates}")

    def record_death(
        self, epoch: int, count: int, region_coordinates: RegionCoordinates
    ) -> None:
        """
        Handle death events by updating the data bank and logger.

        Args:
            epoch: The current epoch of the simulation.
            count: The number of agents that died.
            region_coordinates: The coordinates of the region where the death occurred.

        Returns:
            None

        """
        self.databank.record_deaths(epoch, region_coordinates, count)
        if self.logger:
            self.logger.debug(f"{count} agents died in {region_coordinates}")
