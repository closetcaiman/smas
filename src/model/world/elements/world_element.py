from abc import ABC, abstractmethod


class WorldElement(ABC):
    """
    Abstract base class for elements in the world, such as regions, food resources, etc.

    Methods:
        step_simulation(): Perform one step of the simulation for this world element.

    """

    @abstractmethod
    def step_simulation(self) -> None:
        """Perform one step of the simulation for this world element."""
        raise NotImplementedError("Subclasses must implement step_simulation()")
