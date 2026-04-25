"""Module containing the main World class, which represents the entire simulation environment, including the grid of regions and their interactions."""

from .elements import FoodResources, FoodType, Region
from .world import World

__all__ = ["FoodResources", "FoodType", "Region", "World"]
